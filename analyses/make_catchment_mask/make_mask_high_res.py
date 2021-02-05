#!/usr/bin/env python

# Make a mask on the 20CRv3 PRMSL grid showing which points are in the
#  Yangtze catchment.
# High res version for plotting.


import os
import iris
import numpy
import geopandas
from shapely.geometry import Point
import pickle

# Read the shapefile and extract the polygon for the Yangtze
rivers = geopandas.read_file("Major_Basins_of_the_World.shp")
yangtze = rivers[rivers["NAME"] == "Yangtze"]

def makePlotCube(cs, resolution, xmin, xmax, ymin, ymax):

    lat_values = numpy.arange(ymin, ymax + resolution, resolution)
    latitude = iris.coords.DimCoord(
        lat_values, var_name='latitude',standard_name="grid_latitude", units="degrees_north", coord_system=cs
    )
    lon_values = numpy.arange(xmin, xmax + resolution, resolution)
    longitude = iris.coords.DimCoord(
        lon_values, var_name='longitude',standard_name="grid_longitude", units="degrees_east", coord_system=cs
    )
    dummy_data = numpy.zeros((len(lat_values), len(lon_values)))
    plot_cube = iris.cube.Cube(
        dummy_data, dim_coords_and_dims=[(latitude, 0), (longitude, 1)]
    )
    return plot_cube


rGrid = makePlotCube(
    iris.coord_systems.RotatedGeogCS(90.0, 180.0, 0),
    0.05,
    110 - 40 * 0.5,
    110 + 40 * 0.5,
    30 - 15 * 0.5,
    30 + 15 * 0.5,
)

# Convert the field to an in=1, out=0 mask
lats = rGrid.coord(axis='Y').points
lons = rGrid.coord(axis='X').points
[lon2d, lat2d] = numpy.meshgrid(lons, lats)
lon2 = lon2d.reshape(-1)  # to 1d for iteration
lat2 = lat2d.reshape(-1)
mask = []
for lat, lon in zip(lat2, lon2):
    this_point = geopandas.GeoSeries(
        [Point(lon, lat)], crs=yangtze.crs, index=yangtze.index
    )
    res = yangtze.geometry.contains(this_point)
    mask.append(res.values[0])

mask = numpy.array(mask).reshape(lon2d.shape)
mask = mask * 1
rGrid.data = mask
iris.save(rGrid, "mask.plot.nc")
#pickle.dump(rGrid,open('mask.plot.pkl','wb'))
