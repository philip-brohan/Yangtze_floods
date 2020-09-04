#!/usr/bin/env python

# Plot a map showing the new station locations

import os
import numpy
import pandas
import math
from collections import OrderedDict

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle

import IRData.twcr as twcr

from swirly import plot_cube
from swirly import wind_field
from swirly import normalise_precip
from swirly import normalise_t2m
from swirly import make_z

from pandas import qcut

import datetime

dte = datetime.datetime(1931, 3, 12, 0)

# New station names and positions
from new_stations import get_new_stations

new_stations = get_new_stations()

# Landscape page
aspect = 16 / 9
fig = Figure(
    figsize=(11, 11 / aspect),  # Width, Height (inches)
    dpi=100,
    facecolor=(0.88, 0.88, 0.88, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=False,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)
font = {"family": "sans-serif", "sans-serif": "Arial", "weight": "normal", "size": 12}
matplotlib.rc("font", **font)

ax_full = fig.add_axes([0, 0, 1, 1])
ax_full.set_axis_off()
ax_full.add_patch(Rectangle((0, 0), 1, 1, facecolor=(1, 1, 1, 1), fill=True, zorder=1))

t2m = twcr.load("air.2m", dte, version="4.6.1").extract(iris.Constraint(member=0))
u10m = twcr.load("uwnd.10m", dte, version="4.6.1").extract(iris.Constraint(member=0))
v10m = twcr.load("vwnd.10m", dte, version="4.6.1").extract(iris.Constraint(member=0))
precip = twcr.load("prate", dte, version="4.6.1").extract(iris.Constraint(member=0))
precip = normalise_precip(precip)
obs = twcr.load_observations_fortime(dte, version="4.6.1")
# prmsl all members for spread
prmsl = twcr.load("prmsl", dte, version="4.6.1")
prmsl = prmsl.collapsed("member", iris.analysis.STD_DEV)
# Load the climatological prmsl stdev from v2c

prevt = datetime.datetime(
    dte.year, dte.month, dte.day, int(dte.hour) - int(dte.hour) % 6
)
prevcsd = iris.load_cube(
    "/data/users/hadpb/20CR/version_3.4.1/standard.deviation/prmsl.nc",
    iris.Constraint(
        time=iris.time.PartialDateTime(
            year=1981, month=prevt.month, day=prevt.day, hour=prevt.hour
        )
    ),
)
nextt = prevt + datetime.timedelta(hours=6)
nextcsd = iris.load_cube(
    "/data/users/hadpb/20CR/version_3.4.1/standard.deviation/prmsl.nc",
    iris.Constraint(
        time=iris.time.PartialDateTime(
            year=1981, month=nextt.month, day=nextt.day, hour=nextt.hour
        )
    ),
)
w = (dte - prevt).total_seconds() / (nextt - prevt).total_seconds()
prevcsd.data = prevcsd.data * (1 - w) + nextcsd.data * w
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
prevcsd.coord("latitude").coord_system = coord_s
prevcsd.coord("longitude").coord_system = coord_s


# China-centred projection
scale = 30
extent = [scale * -0.85 * aspect, scale * 0.85 * aspect, scale * -1, scale]
# extent=[-180,180,-90,90]

# Projection for plotting
pole_longitude = 267.5
pole_latitude = 55.5
cs = iris.coord_systems.RotatedGeogCS(pole_latitude, pole_longitude, 0)


# Map with background
ax_map = fig.add_axes([0.003, 0.005, 0.85, 0.99])
ax_map.set_axis_off()
ax_map.set_xlim(extent[0], extent[1])
ax_map.set_ylim(extent[2], extent[3])
ax_map.set_aspect("auto")

# Plot the land mask
mask = iris.load_cube(
    "%s/fixed_fields/land_mask/opfc_global_2019.nc" % os.getenv("DATADIR")
)
mask_pc = plot_cube(cs, 0.05, extent[0], extent[1], extent[2], extent[3])
mask = mask.regrid(mask_pc, iris.analysis.Linear())
lats = mask.coord("latitude").points
lons = mask.coord("longitude").points
mask_img = ax_map.pcolorfast(
    lons,
    lats,
    mask.data,
    cmap=matplotlib.colors.ListedColormap(((0.4, 0.4, 0.4, 0), (0.4, 0.4, 0.4, 1))),
    vmin=0,
    vmax=1,
    alpha=1.0,
    zorder=20,
)
wind_pc = plot_cube(cs, 0.2, extent[0], extent[1], extent[2], extent[3])
rw = iris.analysis.cartography.rotate_winds(u10m, v10m, cs)
u10m = rw[0].regrid(wind_pc, iris.analysis.Linear())
v10m = rw[1].regrid(wind_pc, iris.analysis.Linear())
wind_noise_field = wind_field(
    u10m, v10m, make_z(cs, extent, resolution=0.05), sequence=0, epsilon=0.03
)

t2m_pc = plot_cube(cs, 0.05, extent[0], extent[1], extent[2], extent[3])
t2m = t2m.regrid(t2m_pc, iris.analysis.Linear())
# Adjust to show the wind
wscale = 200
s = wind_noise_field.data.shape
wind_noise_field.data = (
    qcut(
        wind_noise_field.data.flatten(), wscale, labels=False, duplicates="drop"
    ).reshape(s)
    - (wscale - 1) / 2
)

# Plot as a colour map
wnf = wind_noise_field.regrid(t2m, iris.analysis.Linear())
s = t2m.data.shape
t2m.data = qcut(t2m.data.flatten(), 100, labels=False).reshape(s)
t2m_img = ax_map.pcolorfast(
    lons, lats, t2m.data * 10 + wnf.data, cmap="RdYlBu_r", alpha=0.8, zorder=100
)

# Plot the precip
precip_pc = plot_cube(cs, 0.25, extent[0], extent[1], extent[2], extent[3])
precip = normalise_precip(precip.regrid(precip_pc, iris.analysis.Linear()))
wnf = wind_noise_field.regrid(precip, iris.analysis.Linear())
precip.data[precip.data > 0.8] += wnf.data[precip.data > 0.8] / 3000
precip.data[precip.data < 0.8] = 0.8
cols = []
for ci in range(100):
    cols.append([0.0, 0.3, 0.0, ci / 100])
precip_img = ax_map.pcolorfast(
    lons,
    lats,
    precip.data,
    cmap=matplotlib.colors.ListedColormap(cols),
    alpha=0.9,
    zorder=200,
)

# Plot the observations
for i in range(0, len(obs["Longitude"].values)):
    weight = 0.85
    if "weight" in obs.columns:
        weight = obs["weight"].values[i]
    rp = iris.analysis.cartography.rotate_pole(
        numpy.array(obs["Longitude"].values[i]),
        numpy.array(obs["Latitude"].values[i]),
        pole_longitude,
        pole_latitude,
    )
    nlon = rp[0][0]
    nlat = rp[1][0]
    ax_map.add_patch(
        matplotlib.patches.Circle(
            (nlon, nlat),
            radius=0.2,
            facecolor="white",
            edgecolor="black",
            linewidth=1,
            alpha=weight,
            zorder=180,
        )
    )

# Plot the fog of ignorance
fog_pc = plot_cube(cs, 0.25, extent[0], extent[1], extent[2], extent[3])
prmsl = prmsl.regrid(precip_pc, iris.analysis.Linear())
prevcsd = prevcsd.regrid(precip_pc, iris.analysis.Linear())
prmsl.data = numpy.minimum(1, prmsl.data / prevcsd.data)
cols = []


def fog_map(x):
    return 1 / (1 + math.exp((x - 0.5) * -10))


for ci in range(100):
    cols.append([0.8, 0.8, 0.8, fog_map(ci / 100)])

# fog_img = ax_map.pcolorfast(lons, lats, prmsl.data,
#                           cmap=matplotlib.colors.ListedColormap(cols),
#                           alpha=0.95,
#                           zorder=300)


# Label with the date
ax_map.text(
    -44,
    -28.75,
    "%04d-%02d-%02d:%02d" % (dte.year, dte.month, dte.day, dte.hour),
    horizontalalignment="left",
    verticalalignment="bottom",
    color="black",
    bbox=dict(
        facecolor=(0.8, 0.8, 0.8, 0.7), edgecolor="black", boxstyle="round", pad=0.25
    ),
    size=10,
    clip_on=True,
    zorder=5000,
)


# Station labels on the right

# Rotate the station positions into plot coordinates
for i in range(len(new_stations["Longitude"].values)):
    rp = iris.analysis.cartography.rotate_pole(
        numpy.array(new_stations["Longitude"].values[i]),
        numpy.array(new_stations["Latitude"].values[i]),
        pole_longitude,
        pole_latitude,
    )
    new_stations["Longitude"].values[i] = rp[0][0]
    new_stations["Latitude"].values[i] = rp[1][0]

new_stations = new_stations.sort_values(by="Latitude", ascending=True)
new_stations = new_stations.reset_index(drop=True)
stations = list(OrderedDict.fromkeys(new_stations.Name))

# ax_right=fig.add_axes([0.995,0.005,0.005,0.99])
# ax_map.set_axis_off()

# Join each station name to its location on the map


def pos_left(idx):
    new_lon = new_stations["Longitude"].values[idx]
    new_lat = new_stations["Latitude"].values[idx]
    result = {}
    result["x"] = 0.005 + 0.85 * (new_lon - (scale * -1) * aspect * 0.85) / (
        scale * 2 * aspect * 0.85
    )
    result["y"] = 0.005 + 0.99 * (new_lat - (scale * -1)) / (scale * 2)
    return result


# Label location of a station in ax_full coordinates
def pos_right(idx):
    result = {}
    result["x"] = 0.865
    result["y"] = 0.005 + (0.99 / len(stations)) * (idx + 0.5)
    return result


ax_top = fig.add_axes([0, 0, 1, 1], label="top")
ax_top.set_axis_off()
ax_top.set_zorder(10000)

for i in range(len(stations)):
    p_left = pos_left(i)
    p_right = pos_right(i)
    ax_map.add_patch(
        Circle(
            (new_stations["Longitude"].values[i], new_stations["Latitude"].values[i]),
            radius=0.25,
            facecolor="red",
            edgecolor="red",
            linewidth=1,
            alpha=1,
            zorder=1000,
        )
    )
    ax_top.add_patch(
        Circle(
            (p_right["x"] - 0.005, p_right["y"]),
            radius=0.002,
            facecolor=(1, 0, 0, 1),
            edgecolor=(0, 0, 0, 1),
            alpha=1,
            zorder=1000,
        )
    )
    ax_top.text(
        p_right["x"] + 0.005,
        p_right["y"],
        stations[i],
        horizontalalignment="left",
        verticalalignment="center",
        color="black",
        size=10,
        zorder=5000,
    )
    ax_top.add_line(
        matplotlib.lines.Line2D(
            xdata=(p_left["x"], p_right["x"] - 0.005),
            ydata=(p_left["y"], p_right["y"]),
            linestyle="solid",
            linewidth=0.5,
            color=(0, 0, 0, 1.0),
            zorder=9000,
        )
    )

# Output as png
fig.savefig("stations.png")
