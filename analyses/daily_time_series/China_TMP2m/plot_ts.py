#!/usr/bin/env python

# 20CRv3 time-series: Daily average, regional average.
#  Each ensemble member as a seperate line.

# Uses pre-calculated time-series.

import os
import iris
import numpy
import datetime
from calendar import monthrange
import pickle

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

start=datetime.datetime(1930,10,1,0,0)
end=datetime.datetime(1931,9,30,23,59)

ylim = (-10,10)

def fromversion(version):
    dts=[]
    ndata=None
    for year in (1930,1931):
        for month in range (1,13):
            if year == 1930 and month <10: continue
            if year == 1931 and month >9:  continue
            for day in range(1,monthrange(year,month)[1]+1):
                opf="%s/20CR/version_%s/analyses/Yangtze_ts_daily/TMP2m/%04d%02d%02d.pkl" % (
                       os.getenv('SCRATCH'),version,year,month,day)
                with open(opf, "rb") as f:
                    nddy  = pickle.load(f)
                if ndata is None:
                    ndata = nddy
                else:
                    ndata = numpy.ma.concatenate((ndata,nddy))
                dts.append(datetime.datetime(year,month,day,12))
    return (ndata,dts)

# Plot the resulting array as a set of line graphs
fig=Figure(figsize=(19.2,6),              # Width, Height (inches)
           dpi=300,
           facecolor=(0.5,0.5,0.5,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,                
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)

# Plot the lines
ax = fig.add_axes([0.06,0.06,0.93,0.92],
                  xlim=((start-datetime.timedelta(days=1)),
                        (end+datetime.timedelta(days=1))),
                  ylim=ylim)
ax.set_ylabel('T2m anomaly')

(ndata,dts) = fromversion('3')
for m in range(80):
    ax.add_line(Line2D(dts, 
                       ndata[:,m], 
                       linewidth=0.5, 
                       color=(0,0,0,1),
                       alpha=0.1,
                       zorder=200))

(ndata,dts) = fromversion('4.6.1')
for m in range(80):
    ax.add_line(Line2D(dts, 
                       ndata[:,m]+3, 
                       linewidth=0.5, 
                       color=(0,0,1,1),
                       alpha=0.1,
                       zorder=200))

(ndata,dts) = fromversion('4.6.7')
for m in range(80):
    ax.add_line(Line2D(dts, 
                       ndata[:,m]-3, 
                       linewidth=0.5, 
                       color=(1,0,0,1),
                       alpha=0.1,
                       zorder=200))

fig.savefig('TMP2m_ts.png')

