#!/usr/bin/env python

# Plot a map showing the new station locations

import os
import numpy
import pandas
from collections import OrderedDict

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
import IRData.twcr as twcr

# New station names and positions
from new_stations import get_new_stations
new_stations=get_new_stations()

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
scale=25
extent=[scale*-0.8*aspect,scale*0.8*aspect,scale*-1,scale]

# Map with background
ax_map=fig.add_axes([0.005,0.005,0.8,0.99],projection=projection)
ax_map.set_axis_off()
ax_map.set_extent(extent, crs=projection)
ax_map.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_map)
land_img=ax_map.background_img(name='GreyT', resolution='low')

mg.observations.plot(ax_map,new_stations,radius=0.2,
                     facecolor='red',edgecolor='black')

# Station labels on the right
new_stations=new_stations.sort_values(by='Latitude',ascending=True)
new_stations=new_stations.reset_index(drop=True)
stations=list(OrderedDict.fromkeys(new_stations.Name))

ax_right=fig.add_axes([0.995,0.005,0.005,0.99])
# no x-axis
ax_right.set_xlabel('')

ax_right.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_right.yaxis.set_major_locator(
              matplotlib.ticker.FixedLocator(y_locations))
ax_right.yaxis.set_major_formatter(
              matplotlib.ticker.FixedFormatter(
                  [s for s in stations]))


# Join each station name to its location on the map
# Need another axes, filling the whole fig
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0)  # Transparent background

def pos_left(idx):
    station=stations[idx]
    rp=ax_map.projection.transform_points(ccrs.PlateCarree(),
                                             numpy.asarray(new_stations.Longitude[idx]),
                                             numpy.asarray(new_stations.Latitude[idx]))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.005+0.8*(new_lon-(scale*-1)*aspect*0.8)/(scale*2*aspect*0.8)
    result['y']=0.005+0.99*(new_lat-(scale*-1))/(scale*2)
    return result

# Label location of a station in ax_full coordinates
def pos_right(idx):
    result={}
    result['x']=0.83
    result['y']=0.005+(0.99/len(stations))*(idx+0.5)
    return result

for i in range(len(stations)):
    p_left=pos_left(i)
    p_right=pos_right(i)
    ax_full.add_patch(Circle((p_right['x']-0.005,
                              p_right['y']),
                             radius=0.002,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']-0.005),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.5,
            color=(1,0,0,1.0),
            zorder=1))

# Output as png
fig.savefig('stations.png')
