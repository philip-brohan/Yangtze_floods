#!/usr/bin/env python

# Plot a map showing the Yangtze catchment

import os
import numpy

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import cartopy
import cartopy.crs as ccrs

import Meteorographica as mg

# Landscape page
aspect=1.0
fig=Figure(figsize=(11,11/aspect),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 14}
matplotlib.rc('font', **font)

# China-centred projection
projection=ccrs.RotatedPole(pole_longitude=287.5, pole_latitude=55.5)
cs = iris.coord_systems.RotatedGeogCS(55.5, 287.5, 0)
scale=25
extent=[scale*-1*aspect,scale*1*aspect,scale*-1,scale]

# Map with background
ax_map=fig.add_axes([0.0,0.0,1.0,1.0],projection=projection)
ax_map.set_axis_off()
ax_map.set_extent(extent, crs=projection)
ax_map.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_map)
land_img=ax_map.background_img(name='GreyT', resolution='low')

# Load the catchment map
cGrid = iris.load_cube('mask.PRMSL.256x512.nc')
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
cGrid.coord("latitude").coord_system = coord_s
cGrid.coord("longitude").coord_system = coord_s

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

mask_pc = plot_cube(cs, 0.05, extent[0], extent[1], extent[2], extent[3])
mask = cGrid.regrid(mask_pc, iris.analysis.Linear())
lats = mask.coord("latitude").points
lons = mask.coord("longitude").points
mask_img = ax_map.pcolorfast(
    lons,
    lats,
    mask.data,
    cmap=matplotlib.colors.ListedColormap(((1.0, 1.0, 0.0, 0), (1.0, 1.0, 0.0, 0.7))),
    vmin=0,
    vmax=1,
    alpha=1.0,
    zorder=200,
)

# Output as png
fig.savefig('catchment.png')
