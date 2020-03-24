#!/usr/bin/env python

# 20CRv3 time-series: Daily average, regional average.
#  Each ensemble member as a seperate line.
# Show difference from v3 mean, and spread.

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

start=datetime.datetime(1930,4,1,0,0)
end=datetime.datetime(1932,3,31,23,59)

ylim = (-7.5,7.5)

def fromversion(version):
    dts=[]
    spread=[]
    ndata=None
    for year in range(1929,1933):
        for month in range (1,13):
            for day in range(1,monthrange(year,month)[1]+1):
                opf="%s/20CR/version_%s/analyses/Yangtze_ts_daily/TMP2m/%04d%02d%02d.pkl" % (
                       os.getenv('SCRATCH'),version,year,month,day)
                if not os.path.exists(opf): continue
                with open(opf, "rb") as f:
                    nddy  = pickle.load(f)
                if ndata is None:
                    ndata = nddy
                else:
                    ndata = numpy.ma.concatenate((ndata,nddy))
                dts.append(datetime.datetime(year,month,day,12))
                spread.append(numpy.std(nddy))
    return (ndata,dts,spread)

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
ax = fig.add_axes([0.06,0.06,0.93,0.67],
                  xlim=((start-datetime.timedelta(days=1)),
                        (end+datetime.timedelta(days=1))),
                  ylim=ylim)
ax.set_ylabel('TMP2m minus v3 mean')
ax2 = fig.add_axes([0.06,0.75,0.93,0.22],
                  xlim=((start-datetime.timedelta(days=1)),
                        (end+datetime.timedelta(days=1))),
                   ylim=[.1,1.1])
ax2.set_ylabel('Spread')
ax2.get_xaxis().set_visible(False)

(ndata,dts,spread) = fromversion('3')
v3m = numpy.mean(ndata,1)
for m in range(80):
    ax.add_line(Line2D(dts, 
                       ndata[:,m]-v3m, 
                       linewidth=0.5, 
                       color=(0,0,0,1),
                       alpha=0.1,
                       zorder=200))
ax2.add_line(Line2D(dts, 
                    spread, 
                    linewidth=1, 
                    color=(0,0,0,1),
                    alpha=1,
                    zorder=200))


(ndata,dts,spread) = fromversion('4.6.1')
for m in range(80):
    ax.add_line(Line2D(dts, 
                       ndata[:,m]-v3m[365:(365+365)]+4, 
                       linewidth=0.5, 
                       color=(0,0,1,1),
                       alpha=0.1,
                       zorder=200))
ax2.add_line(Line2D(dts, 
                    spread, 
                    linewidth=1, 
                    color=(0,0,1,1),
                    alpha=1,
                    zorder=200))

(ndata,dts,spread) = fromversion('4.6.7')
for m in range(80):
    ax.add_line(Line2D(dts, 
                       ndata[:,m]-v3m[365:(365+365)]-4, 
                       linewidth=0.5, 
                       color=(1,0,0,1),
                       alpha=0.1,
                       zorder=200))
ax2.add_line(Line2D(dts, 
                    spread, 
                    linewidth=1, 
                    color=(1,0,0,1),
                    alpha=1,
                    zorder=200))

fig.savefig('TMP2m_dts_s.png')

