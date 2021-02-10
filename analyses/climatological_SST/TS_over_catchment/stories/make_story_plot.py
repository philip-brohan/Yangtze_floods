#!/usr/bin/env python

# 20CRv3 time-series: 3-hourly data, catchment average.
#  Each ensemble member as a seperate line.

# Uses pre-calculated time-series.

# Also has maps at selected times.

import os
import sys
import iris
import numpy
import datetime
import pickle
import math

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

sys.path.append("%s/." % os.path.dirname(__file__))
from miniMap import miniMap

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--startyear", help="Start Year", type=int, default=1930, required=False
)
parser.add_argument(
    "--startmonth", help="Start Month", type=int, default=10, required=False
)
parser.add_argument("--startday", help="Start Day", type=int, default=1, required=False)
parser.add_argument(
    "--starthour", help="Start Hour", type=int, default=6, required=False
)
parser.add_argument(
    "--endyear", help="End Year", type=int, default=1931, required=False
)
parser.add_argument("--endmonth", help="End Month", type=int, default=9, required=False)
parser.add_argument("--endday", help="End Day", type=int, default=30, required=False)
parser.add_argument("--endhour", help="End Hour", type=int, default=18, required=False)
parser.add_argument("--var", help="Variable to plot", type=str, required=True)
parser.add_argument(
    "--version",
    help="20CR version ('3' or e.g. '4.6.5')",
    default="3",
    type=str,
    required=False,
)
parser.add_argument(
    "--comparison",
    help="20CR version ('3' or e.g. '4.6.5')",
    default=None,
    type=str,
    required=False,
)
parser.add_argument(
    "--ymin", help="Y-axis minimum", type=float, default=None, required=False
)
parser.add_argument(
    "--ymax", help="Y-axis maximum", type=float, default=None, required=False
)
parser.add_argument(
    "--yscale", help="Y-axis scale factor", type=float, default=1.0, required=False
)
parser.add_argument(
    "--yfigscale", help="Figure Y scale factor", type=float, default=1.0, required=False
)
parser.add_argument(
    "--map",
    help="Minimap specification string",
    type=str,
    default=None,
    required=False,
    action="append",
)
args = parser.parse_args()
start = datetime.datetime(
    args.startyear, args.startmonth, args.startday, args.starthour
)
end = datetime.datetime(args.endyear, args.endmonth, args.endday, args.endhour)

# Decode the map specification
def decodeSpec(mapSpec):
    result = {}
    mYear = int(mapSpec[0:4])
    mMonth = int(mapSpec[5:7])
    mDay = int(mapSpec[8:10])
    mHour = int(mapSpec[11:13])
    result["mdte"] = datetime.datetime(mYear, mMonth, mDay, mHour)
    pYear = int(mapSpec[14:18])
    pMonth = int(mapSpec[19:21])
    pDay = int(mapSpec[22:24])
    pHour = int(mapSpec[25:27])
    result["pdte"] = datetime.datetime(pYear, pMonth, pDay, pHour)
    resid = mapSpec[28:]
    if resid.find("_") == -1:
        result["ypos"] = float(resid)
        result["scale"] = 1.0
    else:
        result["ypos"] = float(resid[: resid.find("_")])
        result["scale"] = float(resid[(resid.find("_") + 1) :])
    return result


def fromversion(version, year_offset=0):
    dts = []
    ndata = None
    lstart = datetime.datetime(
        start.year + year_offset, start.month, start.day, start.hour
    ) - datetime.timedelta(days=30)
    lend = datetime.datetime(
        end.year + year_offset, end.month, end.day, end.hour
    ) + datetime.timedelta(days=30)
    current = lstart
    while current <= lend:
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
        if not (current.month == 2 and current.day == 29):
            if os.path.exists(opf):
                with open(opf, "rb") as f:
                    nddy = pickle.load(f)
                if ndata is None:
                    ndata = numpy.reshape(nddy, [1, 80])
                else:
                    ndata = numpy.ma.concatenate((ndata, numpy.reshape(nddy, [1, 80])))
                dts.append(
                    datetime.datetime(
                        current.year - year_offset,
                        current.month,
                        current.day,
                        current.hour,
                    )
                )
        current += datetime.timedelta(hours=3)
    return (ndata, dts)


# Calculate the ensemble average
def ensm(values):
    return numpy.mean(values, axis=1)


# Calculate a running mean
def movingaverage(dates, values, window):
    weights = numpy.repeat(1.0, window) / window
    sma = numpy.convolve(values, weights, "valid")
    # same processing on the dates array
    epoch = dates[0]
    dates = numpy.array([(d - epoch).total_seconds() for d in dates])
    dms = numpy.convolve(dates, weights, "valid").tolist()
    dms = [epoch + datetime.timedelta(seconds=d) for d in dms]
    return (dms, sma)


# Get the 3-hourly data
(ndata, dts) = fromversion(args.version, year_offset=0)

if args.ymin is None:
    args.ymin = numpy.amin(ndata) * args.yscale
if args.ymax is None:
    args.ymax = numpy.amax(ndata) * args.yscale

# Convert units between axes units (for plotting) and figure units
#  (for axes locations).
def figureToAxes(x, y):
    frx = (x - 0.06) / 0.93
    ftx = start + datetime.timedelta(seconds=int((end - start).total_seconds() * frx))
    fry = (y - 0.06) / 0.92
    fty = args.ymin + (args.ymax - args.ymin) * fry
    return (ftx, fty)


def axesToFigure(x, y):
    frx = (x - start).total_seconds() / (end - start).total_seconds()
    ftx = frx * 0.93 + 0.06
    fry = (y - args.ymin) / (args.ymax - args.ymin)
    fty = fry * 0.92 + 0.06
    return (ftx, fty)


# Expand the range if necessary to fit in the figures
if args.map is not None:
    for mapSpec in args.map:
        dSpec = decodeSpec(mapSpec)
        if dSpec["ypos"] + dSpec["scale"] * (args.ymax - args.ymin) / 6 > args.ymax:
            args.ymax = dSpec["ypos"] + dSpec["scale"] * (args.ymax - args.ymin) / 6
        if dSpec["ypos"] - dSpec["scale"] * (args.ymax - args.ymin) / 6 < args.ymin:
            args.ymin = dSpec["ypos"] - dSpec["scale"] * (args.ymax - args.ymin) / 6

# Plot the resulting array as a set of line graphs
fig = Figure(
    figsize=(19.2, 6 * args.yfigscale),  # Width, Height (inches)
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

ax = fig.add_axes(
    [0.06, 0.06, 0.93, 0.92],
    xlim=((start - datetime.timedelta(days=1)), (end + datetime.timedelta(days=1))),
    ylim=(args.ymin, args.ymax),
)
if args.yscale == 1:
    ax.set_ylabel(args.var)
else:
    ax.set_ylabel("%s (*%g)" % (args.var, args.yscale))

# Add monthly boundary lines
for yr in range(start.year, end.year + 1):
    for mo in range(1, 13):
        mbdt = datetime.datetime(yr, mo, 1, 0)
        if mbdt > start and mbdt < end:
            ax.add_line(
                Line2D(
                    [mbdt, mbdt],
                    [args.ymin, args.ymax],
                    linewidth=0.25,
                    color=(0, 0, 0, 1),
                    alpha=1.0,
                    zorder=100,
                )
            )

# 3-hourly, all ensemble members
for m in range(80):
    ax.add_line(
        Line2D(
            dts,
            ndata[:, m] * args.yscale,
            linewidth=0.5,
            color=(0, 0, 0, 1),
            alpha=0.02,
            zorder=200,
        )
    )

# Add the running mean of the ensemble mean
(edtsrm, ermem) = movingaverage(dts, ensm(ndata) * args.yscale, 3 * 8)
ax.add_line(
    Line2D(
        edtsrm,
        ermem,
        linewidth=2.0,
        color=(0, 0, 0, 1),
        alpha=1,
        zorder=300,
    )
)

if args.comparison is not None:
    # Add the running mean of the ensemble mean for the comparison dataset
    (nd2, dts2) = fromversion(args.comparison)
    (dtsrm, rmem) = movingaverage(dts2, ensm(nd2) * args.yscale, 3 * 8)
    ax.add_line(
        Line2D(
            dtsrm,
            rmem,
            linewidth=2.0,
            color=(1, 0, 0, 1),
            alpha=1,
            zorder=250,
        )
    )

ndd_a = None
ndd_c = 0
for dec in [-4, -3, -2, -1, 1, 2, 3, 4]:
    # Add the running mean of the ensemble mean for the comparison dataset
    (ndd, dtsd) = fromversion(args.version, year_offset=dec)
    (dtsrm, rmem) = movingaverage(dtsd, ensm(ndd) * args.yscale, 3 * 8)
    if ndd_a is None:
        ndd_a = ndd.copy()
    else:
        ndd_a += ndd
    ndd_c += 1
    ax.add_line(
        Line2D(
            dtsrm,
            rmem,
            linewidth=1.0,
            color=(0, 0, 1, 1),
            alpha=0.25,
            zorder=150,
        )
    )
(dtsrm, rmem) = movingaverage(dtsd, ensm(ndd_a) * args.yscale / ndd_c, 30 * 8)
ax.add_line(
    Line2D(
        dtsrm,
        rmem,
        linewidth=2.0,
        color=(0, 0, 1, 1),
        alpha=0.5,
        zorder=175,
    )
)


# Add a map of the 3-day mean
def addMap(dtime, x, y, scale=1.0):
    size = 0.12 * scale
    figC = axesToFigure(x, y)
    ax_map = fig.add_axes(
        [figC[0] - size / 2, figC[1] - size * 0.9, size, size * 1.8 / args.yfigscale],
    )
    ax_map.set_axis_off()
    miniMap(
        ax_map,
        dtime.year,
        dtime.month,
        dtime.day,
        dtime.hour,
        args.var,
        xscale=48,
        yscale=27,
    )
    # Link the map to its point on the curve
    cdte = edtsrm.index(dtime - datetime.timedelta(minutes=90))
    cx = edtsrm[cdte]
    cy = ermem[cdte]
    axCB = figureToAxes(figC[0], figC[1] - size * 0.9)
    axCT = figureToAxes(figC[0], figC[1] + size * 0.9)
    if abs(axCT[1] - cy) > abs(axCB[1] - cy):
        axC = axCB
    else:
        axC = axCT
    ax.add_line(
        Line2D(
            [axC[0], cx],
            [axC[1], cy],
            linewidth=1.0,
            color=(0, 0, 0, 1),
            alpha=1.0,
            zorder=1,
        )
    )


if args.map is not None:
    for mapSpec in args.map:
        dSpec = decodeSpec(mapSpec)
        addMap(dSpec["mdte"], dSpec["pdte"], dSpec["ypos"], scale=dSpec["scale"])

fig.savefig("%s_story.png" % args.var)
