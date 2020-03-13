#!/usr/bin/env python

# Plot v4.6.1, v4.6.7 and the results at the new stations

import os
import math
import datetime
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

# Date to show
year=1930
month=11
day=1
hour=0
dte=datetime.datetime(year,month,day,hour)

# New station names and positions
from new_stations import get_new_stations
new_stations=get_new_stations()

# Landscape page
aspect=16/9.0
fig=Figure(figsize=(22,22/aspect),  # Width, Height (inches)
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
extent=[scale*-1*aspect/3.0,scale*aspect/3.0,scale*-1,scale]

# On the left - spaghetti-contour plot of scout 4.6.1
ax_left=fig.add_axes([0.005,0.01,0.323,0.98],projection=projection)
ax_left.set_axis_off()
ax_left.set_extent(extent, crs=projection)
ax_left.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_left)
land_img_left=ax_left.background_img(name='GreyT', resolution='low')

# 4.6.1 data
prmsl=twcr.load('prmsl',dte,version='4.6.1')
obs_t=twcr.load_observations_fortime(dte,version='4.6.1')

# Plot the observations
mg.observations.plot(ax_left,obs_t,radius=0.2)

# PRMSL spaghetti plot
mg.pressure.plot(ax_left,prmsl,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_s.data>300)]=numpy.nan
mg.pressure.plot(ax_left,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=1)

mg.utils.plot_label(ax_left,
              'Scout 4.6.1',
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')

mg.utils.plot_label(ax_left,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.96,
              horizontalalignment='right')

# In the centre - spaghetti-contour plot of v4.6.7
ax_centre=fig.add_axes([0.335,0.01,0.323,0.98],projection=projection)
ax_centre.set_axis_off()
ax_centre.set_extent(extent, crs=projection)
ax_centre.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_centre)
land_img_centre=ax_centre.background_img(name='GreyT', resolution='low')

prmsl_s=twcr.load('prmsl',dte,version='4.6.7')
obs_t_s=twcr.load_observations_fortime(dte,version='4.6.7')

# Plot the observations
mg.observations.plot(ax_centre,new_stations,radius=0.1,
                     facecolor='red',edgecolor='yellow')
mg.observations.plot(ax_centre,obs_t_s,radius=0.2)

# PRMSL spaghetti plot
mg.pressure.plot(ax_centre,prmsl_s,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl_s.collapsed('member', iris.analysis.MEAN)
prmsl_v=prmsl_s.collapsed('member', iris.analysis.STD_DEV)
prmsl_m.data[numpy.where(prmsl_v.data>300)]=numpy.nan
mg.pressure.plot(ax_centre,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(875,1050,10),
                   colors='black',
                   label=True,
                   linewidths=1)

mg.utils.plot_label(ax_centre,
              'Scout 4.6.7',
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.04,
              horizontalalignment='left')

# Validation scatterplot on the right
new_stations=new_stations.sort_values(by='Latitude',ascending=True)
new_stations=new_stations.reset_index(drop=True)
stations=list(OrderedDict.fromkeys(new_stations.Name))

ax_right=fig.add_axes([0.74,0.05,0.255,0.94])
# x-axis
xrange=[1000,1031]
ax_right.set_xlim(xrange)
ax_right.set_xlabel('')

ax_right.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_right.yaxis.set_major_locator(
              matplotlib.ticker.FixedLocator(y_locations))
ax_right.yaxis.set_major_formatter(
              matplotlib.ticker.FixedFormatter(
                  [s for s in stations]))

for y in range(0,len(stations)):
    ax_right.add_line(matplotlib.lines.Line2D(
            xdata=xrange,
            ydata=(y+1,y+1),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))

# For each station, plot the 4.6.1 ensemble at that station
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                   ['latitude', 'longitude'])
# Keep the ensemble mean to work out the effective ob
ensm=[]
for y in range(len(stations)):
    station=stations[y]
    ensemble=interpolator([new_stations.Latitude[y],
                           new_stations.Longitude[y]])
    ensm.append(numpy.mean(ensemble.data)/100)

    ax_right.scatter(ensemble.data/100.0,
                numpy.linspace(y+1.5,y+1.9,
                              num=len(ensemble.data)),
                20,
                'blue', # Color
                marker='.',
                edgecolors='face',
                linewidths=0.0,
                alpha=0.5,
                zorder=0.5)

# For each station, plot the observed pressure at that station
# Using the 4.6.1 bias estimates
for y in range(0,len(stations)):
    obsn = obs_t[obs_t['ID']==new_stations.ID[y]]
    if obsn.empty: continue
    obsn=obsn.iloc[0,:] # if several, just take the first
    obsn_dt=datetime.datetime(int(obsn['UID'][0:4]),
                              int(obsn['UID'][4:6]),
                              int(obsn['UID'][6:8]),
                              int(obsn['UID'][8:10]))
    tdiff=abs((dte-obsn_dt).total_seconds())
    alpha=max(0,1-tdiff/10000)
    obsn_d=ensm[y]+obsn['Obfit.post']
    ax_right.add_line(matplotlib.lines.Line2D(
            xdata=(obsn_d,obsn_d), ydata=(y+1.5,y+1.9),
            linestyle='solid',
            linewidth=3,
            color=(0,0,0,alpha),
            zorder=1))

# For each station, plot the 4.6.7 ensemble at that station
interpolator = iris.analysis.Linear().interpolator(prmsl_s, 
                                   ['latitude', 'longitude'])
# Keep the ensemble mean to work out the effective ob
ensm=[]
for y in range(len(stations)):
    station=stations[y]
    ensemble=interpolator([new_stations.Latitude[y],
                           new_stations.Longitude[y]])
    ensm.append(numpy.mean(ensemble.data)/100)

    ax_right.scatter(ensemble.data/100.0,
                numpy.linspace(y+1.1,y+1.5,
                              num=len(ensemble.data)),
                20,
                'red', # Color
                marker='.',
                edgecolors='face',
                linewidths=0.0,
                alpha=0.5,
                zorder=0.5)

# For each station, plot the observed pressure at that station
for y in range(0,len(stations)):
    obsn = obs_t_s[obs_t_s['ID']==new_stations.ID[y]]
    if obsn.empty: continue
    obsn=obsn.iloc[0,:] # if several, just take the first
    obsn_dt=datetime.datetime(int(obsn['UID'][0:4]),
                              int(obsn['UID'][4:6]),
                              int(obsn['UID'][6:8]),
                              int(obsn['UID'][8:10]))
    tdiff=abs((dte-obsn_dt).total_seconds())
    alpha=max(0,1-tdiff/10000)
    obsn_d=ensm[y]+obsn['Obfit.post']
    ax_right.add_line(matplotlib.lines.Line2D(
            xdata=(obsn_d,obsn_d), ydata=(y+1.1,y+1.5),
            linestyle='solid',
            linewidth=3,
            color=(0,0,0,alpha),
            zorder=1))

# Join each station name to its location on the map
# Need another axes, filling the whole fig
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0)  # Transparent background

def pos_left(idx):
    station=stations[idx]
    rp=ax_centre.projection.transform_points(ccrs.PlateCarree(),
                                             numpy.asarray(new_stations.Longitude[idx]),
                                             numpy.asarray(new_stations.Latitude[idx]))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.335+0.323*(new_lon-(scale*-1)*aspect/3.0)/(scale*2*aspect/3.0)
    result['y']=0.01+0.98*(new_lat-(scale*-1))/(scale*2)
    return result

# Label location of a station in ax_full coordinates
def pos_right(idx):
    result={}
    result['x']=0.668
    result['y']=0.05+(0.94/len(stations))*(idx+0.5)
    return result

for i in range(len(stations)):
    p_left=pos_left(i)
    if p_left['x']<0.335 or p_left['x']>(0.335+0.323): continue
    if p_left['y']<0.005 or p_left['y']>(0.005+0.94): continue
    p_right=pos_right(i)
    ax_full.add_patch(Circle((p_right['x']-0.005,
                              p_right['y']),
                             radius=0.001,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']-0.005),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(1,0,0,1.0),
            zorder=1))

# Output as png
fig.savefig('v461_v_v467_%04d%02d%02d%02d.png' % 
                                  (year,month,day,hour))
