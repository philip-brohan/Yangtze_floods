#!/usr/bin/env python

# 20CRv3 time-series: Monthly average, Yangtze basin average.
#  Each ensemble member as a seperate line.

# Uses pre-calculated time-series.

import os
import numpy
import pickle

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

opdir="%s/20CR/version_3/analyses/Yangtze_catchment_ts/PRATE" % os.getenv('SCRATCH')

# Get the 1961-90 climatology
clim = []
for month in range(1,13):
    mClim=0
    for year in range(1961,1991):
        cspf = "%s/%04d%02d.pkl" % (opdir,year,month)
        with open( cspf, "rb" ) as pfile:
            mtmp= pickle.load(pfile)
            mClim += sum(mtmp)/len(mtmp)
    clim.append(mClim/30)

# load the anomaly quantiles
cspf = "%s/anomaly_quantiles.pkl" % opdir
with open( cspf, "rb" ) as pfile:
    qts = pickle.load(pfile)

def to_quantile(value):
    qtl = (len(qts[qts<value])+0.5)/len(qts)
    return qtl

# Get the time-series for 1926-1936
dts = []
tSeries = []
for member in range(80):
    tSeries.append([])
for year in range(1926,1937):
    for month in range(1,13):
        cspf = "%s/%04d%02d.pkl" % (opdir,year,month)
        with open( cspf, "rb" ) as pfile:
            mtmp= pickle.load(pfile)
        for member in range(len(mtmp)):
            tSeries[member].append(to_quantile((mtmp[member]-clim[month-1])))
        dts.append(year+(month-0.5)/12)
 
# Make the plot
fig=Figure(figsize=(19.2,6),              # Width, Height (inches)
           dpi=100,
           facecolor=(0.5,0.5,0.5,1),
           edgecolor='black',
           linewidth=1.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)
# Paint the background
ax_full = fig.add_axes([0, 0, 1, 1])
ax_full.set_xlim([0, 1])
ax_full.set_ylim([0, 1])
ax_full.set_axis_off()
ax_full.add_patch(
    Rectangle(
        (0, 0), 1, 1, fill=True, facecolor='white'
    )
)

ax = fig.add_axes([0.04,0.07,0.95,0.92])
ax.set_xlim(xmin=1926,xmax=1937),
ax.set_ylim(ymin=0,ymax=1)
ax.set_xticks([1927,1928,1929,1930,1931,1932,1933,1934,1935])
ax.set_ylabel('PRATE anomaly quantile')

# Mark the median line
ax.add_line(Line2D((1926,1937),(0.5,0.5),
                   linewidth=1.0,
                   color=(0,0,0,0.5),
                   alpha=1.0,
                   zorder=100))

# Mark the flood period
ax.add_patch(
    Rectangle(
        (1931.5, -100), 0.3, 200, fill=True, facecolor=(0,0,0,0.1)
    )
)


for member in range(80):
    ax.add_line(Line2D(dts,tSeries[member],
                       linewidth=0.5,
                       color=(0,0,1,1),
                       alpha=0.1,
                       zorder=200))

fig.savefig('PRATE_quantiles_ts.png')


