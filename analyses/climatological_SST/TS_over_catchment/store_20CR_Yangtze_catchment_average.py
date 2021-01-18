#!/usr/bin/env python

# Extract data from 20CRv3 (or a scout run) at a given time,
#  averaged over the Yangtze catchment,
#   and store the value on SCRATCH.

import IRData.twcr as twcr
import iris
import iris.analysis
import iris.analysis.cartography
import numpy
import datetime
import pickle
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument("--month", help="Month", type=int, required=True)
parser.add_argument("--day", help="Day", type=int, required=True)
parser.add_argument("--hour", help="Hour (and fraction)", type=float, required=True)
parser.add_argument("--var", help="Variable to extract", type=str, required=True)
parser.add_argument(
    "--version",
    help="20CR version ('3' or e.g. '4.6.5')",
    default="3",
    type=str,
    required=True,
)
parser.add_argument(
    "--opdir",
    help="Directory for output files",
    default="%s/20CRv3_Yangtze_data" % os.getenv("SCRATCH"),
    type=str,
    required=False,
)
args = parser.parse_args()

args.opdir = "%s/version_%s/%s/%04d/%02d/%02d" % (
    args.opdir,
    args.version,
    args.var,
    args.year,
    args.month,
    args.day,
)
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

# Get the catchment mask
cGrid = iris.load_cube(
    "%s/../../make_catchment_mask/mask.PRMSL.256x512.nc" % os.path.dirname(__file__)
)
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
cGrid.coord("latitude").coord_system = coord_s
cGrid.coord("longitude").coord_system = coord_s

dte = datetime.datetime(
    args.year, args.month, args.day, int(args.hour), int((args.hour % 1) * 60)
)
rdata = twcr.load(args.var, dte, version=args.version)
rdata.coord("latitude").guess_bounds()
rdata.coord("longitude").guess_bounds()
grid_areas = iris.analysis.cartography.area_weights(rdata)
cGrid = cGrid.regrid(rdata, iris.analysis.Linear())
mdata = iris.util.broadcast_to_shape(cGrid.data, rdata.data.shape, (1, 2))
rdata.data = numpy.ma.masked_where(mdata < 0.5, rdata.data)
ensemble = rdata.collapsed(
    ["longitude", "latitude"], iris.analysis.MEAN, weights=grid_areas
)

pickle.dump(
    ensemble.data.data,
    open(
        "%s/%02d_%02d.pkl" % (args.opdir, int(args.hour), int((args.hour % 1) * 60)),
        "wb",
    ),
)
