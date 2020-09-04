# Atmospheric state - near-surface temperature, wind, and precip.

import os
import IRData.twcr as twcr
import datetime
import pickle

import iris
import numpy
import math

from pandas import qcut

# Remap the precipitation to standardise the distribution
# Normalise a precip field to fixed quantiles
def normalise_precip(p):
    res = p.copy()
    res.data[res.data <= 2.00e-5] = 0.79
    res.data[res.data < 2.10e-5] = 0.81
    res.data[res.data < 2.50e-5] = 0.83
    res.data[res.data < 3.10e-5] = 0.85
    res.data[res.data < 3.80e-5] = 0.87
    res.data[res.data < 4.90e-5] = 0.89
    res.data[res.data < 6.60e-5] = 0.91
    res.data[res.data < 9.10e-5] = 0.93
    res.data[res.data < 13.4e-5] = 0.95
    res.data[res.data < 22.0e-5] = 0.97
    res.data[res.data < 0.79] = 0.99
    return res


# Remap the temperature similarly
def normalise_t2m(p):
    res = p.copy()
    res.data[res.data > 300.10] = 0.95
    res.data[res.data > 299.9] = 0.90
    res.data[res.data > 298.9] = 0.85
    res.data[res.data > 297.5] = 0.80
    res.data[res.data > 295.7] = 0.75
    res.data[res.data > 293.5] = 0.70
    res.data[res.data > 290.1] = 0.65
    res.data[res.data > 287.6] = 0.60
    res.data[res.data > 283.7] = 0.55
    res.data[res.data > 280.2] = 0.50
    res.data[res.data > 277.2] = 0.45
    res.data[res.data > 274.4] = 0.40
    res.data[res.data > 272.3] = 0.35
    res.data[res.data > 268.3] = 0.30
    res.data[res.data > 261.4] = 0.25
    res.data[res.data > 254.6] = 0.20
    res.data[res.data > 249.1] = 0.15
    res.data[res.data > 244.9] = 0.10
    res.data[res.data > 240.5] = 0.05
    res.data[res.data > 0.95] = 0.0
    return res


def plot_cube(cs, resolution, xmin, xmax, ymin, ymax):

    lat_values = numpy.arange(ymin, ymax + resolution, resolution)
    latitude = iris.coords.DimCoord(
        lat_values, standard_name="latitude", units="degrees_north", coord_system=cs
    )
    lon_values = numpy.arange(xmin, xmax + resolution, resolution)
    longitude = iris.coords.DimCoord(
        lon_values, standard_name="longitude", units="degrees_east", coord_system=cs
    )
    dummy_data = numpy.zeros((len(lat_values), len(lon_values)))
    plot_cube = iris.cube.Cube(
        dummy_data, dim_coords_and_dims=[(latitude, 0), (longitude, 1)]
    )
    return plot_cube


# Make the wind noise
def wind_field(uw, vw, z, sequence=None, iterations=50, epsilon=0.003, sscale=1):
    # Random field as the source of the distortions
    z = z.regrid(uw, iris.analysis.Linear())
    (width, height) = z.data.shape
    # Each point in this field has an index location (i,j)
    #  and a real (x,y) position
    xmin = numpy.min(uw.coords()[0].points)
    xmax = numpy.max(uw.coords()[0].points)
    ymin = numpy.min(uw.coords()[1].points)
    ymax = numpy.max(uw.coords()[1].points)
    # Convert between index and real positions
    def i_to_x(i):
        return xmin + (i / width) * (xmax - xmin)

    def j_to_y(j):
        return ymin + (j / height) * (ymax - ymin)

    def x_to_i(x):
        return numpy.minimum(
            width - 1,
            numpy.maximum(0, numpy.floor((x - xmin) / (xmax - xmin) * (width - 1))),
        ).astype(int)

    def y_to_j(y):
        return numpy.minimum(
            height - 1,
            numpy.maximum(0, numpy.floor((y - ymin) / (ymax - ymin) * (height - 1))),
        ).astype(int)

    i, j = numpy.mgrid[0:width, 0:height]
    x = i_to_x(i)
    y = j_to_y(j)
    # Result is a distorted version of the random field
    result = z.copy()
    # Repeatedly, move the x,y points according to the vector field
    #  and update result with the random field at their locations
    ss = uw.copy()
    ss.data = numpy.sqrt(uw.data ** 2 + vw.data ** 2)
    if sequence is not None:
        startsi = numpy.arange(0, iterations, 3)
        endpoints = numpy.tile(startsi, 1 + (width * height) // len(startsi))
        endpoints += sequence % iterations
        endpoints[endpoints >= iterations] -= iterations
        startpoints = endpoints - 25
        startpoints[startpoints < 0] += iterations
        endpoints = endpoints[0 : (width * height)].reshape(width, height)
        startpoints = startpoints[0 : (width * height)].reshape(width, height)
    else:
        endpoints = iterations + 1
        startpoints = -1
    for k in range(iterations):
        x += epsilon * vw.data[i, j]
        x[x > xmax] = xmax
        x[x < xmin] = xmin
        y += epsilon * uw.data[i, j]
        y[y > ymax] = y[y > ymax] - ymax + ymin
        y[y < ymin] = y[y < ymin] - ymin + ymax
        i = x_to_i(x)
        j = y_to_j(y)
        update = z.data * ss.data / sscale
        update[(endpoints > startpoints) & ((k > endpoints) | (k < startpoints))] = 0
        update[(startpoints > endpoints) & ((k > endpoints) & (k < startpoints))] = 0
        result.data[i, j] += update
    return result


def make_z(cs, extent, resolution=0.2):
    z = plot_cube(cs, resolution, extent[0], extent[1], extent[2], extent[3])
    (width, height) = z.data.shape
    z.data = numpy.random.rand(width, height) - 0.5

    z2 = plot_cube(cs, resolution * 2, extent[0], extent[1], extent[2], extent[3])
    (width, height) = z2.data.shape
    z2.data = numpy.random.rand(width, height) - 0.5
    z2 = z2.regrid(z, iris.analysis.Linear())
    z.data = z.data + z2.data

    z4 = plot_cube(cs, resolution * 4, extent[0], extent[1], extent[2], extent[3])
    (width, height) = z4.data.shape
    z4.data = numpy.random.rand(width, height) - 0.5
    z4 = z4.regrid(z, iris.analysis.Linear())
    z.data = z.data + z4.data * 100
    return z
