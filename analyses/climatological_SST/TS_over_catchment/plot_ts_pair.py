#!/usr/bin/env python

# 20CRv3 time-series: 3-hourly data, catchment average.
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

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--startyear", help="Start Year", type=int, required=True)
parser.add_argument("--startmonth", help="Start Month", type=int, required=True)
parser.add_argument("--startday", help="Start Day", type=int, required=True)
parser.add_argument("--starthour", help="Start Hour", type=int, required=True)
parser.add_argument("--endyear", help="End Year", type=int, required=True)
parser.add_argument("--endmonth", help="End Month", type=int, required=True)
parser.add_argument("--endday", help="End Day", type=int, required=True)
parser.add_argument("--endhour", help="End Hour", type=int, required=True)
parser.add_argument("--var", help="Variable to plot", type=str, required=True)
parser.add_argument(
    "--version",
    help="20CR version ('3' or e.g. '4.6.5')",
    default="3",
    type=str,
    required=True,
)
parser.add_argument(
    "--comparison",
    help="20CR version ('3' or e.g. '4.6.5')",
    default="3",
    type=str,
    required=True,
)
args = parser.parse_args()
start = datetime.datetime(
    args.startyear, args.startmonth, args.startday, args.starthour
)
end = datetime.datetime(args.endyear, args.endmonth, args.endday, args.endhour)

ylim = (0, 3.5)


def fromversion(version):
    dts = []
    ndata = None
    current = start
    while current <= end:
        opf = "%s/20CRv3_Yangtze_data/version_%s/%s/%04d/%02d/%02d/%02d_00.pkl" % (
            os.getenv("SCRATCH"),
            version,
            args.var,
            current.year,
            current.month,
            current.day,
            current.hour,
        )
        # Skip leap days to simplify inter-year comparisons
        if current.month == 2 and current.day == 29:
            continue
        if os.path.exists(opf):
            with open(opf, "rb") as f:
                nddy = pickle.load(f)
            if ndata is None:
                ndata = numpy.reshape(nddy, [1, 80])
            else:
                ndata = numpy.ma.concatenate((ndata, numpy.reshape(nddy, [1, 80])))
            dts.append(
                datetime.datetime(
                    current.year, current.month, current.day, current.hour
                )
            )
        current += datetime.timedelta(hours=3)
    return (ndata, dts)


# Calculate the ensemble average
def ensm(values):
    return numpy.mean(values, axis=1)


# Calculate a running mean
def movingaverage(values, window):
    weights = numpy.repeat(1.0, window) / window
    sma = numpy.convolve(values, weights, "same")
    return sma


# Plot the resulting array as a set of line graphs
fig = Figure(
    figsize=(19.2, 6),  # Width, Height (inches)
    dpi=300,
    facecolor=(0.5, 0.5, 0.5, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=False,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)
font = {"family": "sans-serif", "sans-serif": "Arial", "weight": "normal", "size": 16}
matplotlib.rc("font", **font)
axb = fig.add_axes([0, 0, 1, 1])

# Plot the lines
ax = fig.add_axes(
    [0.06, 0.06, 0.93, 0.92],
    xlim=((start - datetime.timedelta(days=1)), (end + datetime.timedelta(days=1))),
    ylim=ylim,
)
ax.set_ylabel("PRATE (*10,000)")

(ndata, dts) = fromversion(args.version)
(nd2, dts2) = fromversion(args.comparison)
for m in range(80):
    ax.add_line(
        Line2D(
            dts,
            ndata[:, m] * 10000,
            linewidth=0.5,
            color=(0, 0, 0, 1),
            alpha=0.02,
            zorder=200,
        )
    )

# Add the running mean of the ensemble mean
ax.add_line(
    Line2D(
        dts,
        movingaverage(ensm(ndata) * 10000, 3 * 8),
        linewidth=2.0,
        color=(0, 0, 0, 1),
        alpha=1,
        zorder=300,
    )
)

# Add the running mean of the ensemble mean for the comparison dataset
ax.add_line(
    Line2D(
        dts,
        movingaverage(ensm(nd2) * 10000, 3 * 8),
        linewidth=2.0,
        color=(1, 0, 0, 1),
        alpha=1,
        zorder=250,
    )
)

fig.savefig("%s_ts_c.png" % args.var)
