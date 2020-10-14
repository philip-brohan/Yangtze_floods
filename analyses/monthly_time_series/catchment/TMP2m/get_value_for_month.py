#!/usr/bin/env python

# Get the mean TMP2m over the Yangtze basin for a selected month.

import os
import numpy
import iris
import pickle
import datetime

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Month",
                    type=int,required=True)
parser.add_argument("--opdir", help="Directory for output files",
                    default="%s/20CR/version_3/analyses/Yangtze_catchment_ts/TMP2m" % \
                                           os.getenv('SCRATCH'),
                    type=str,required=False)
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

# Fix dask SPICE bug
import dask
dask.config.set(scheduler='single-threaded')

# Get the catchment mask
cGrid = iris.load_cube('../../../make_catchment_mask/mask.PRMSL.256x512.nc')

# 80 members
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
mTMP2m = []

for member in range(80):

    # Get the monthly PRMSL field
    pField = iris.load_cube(
        '%s/20CR/version_3/monthly/%04d/TMP2m.%04d.mnmean_mem%03d.nc' 
        % (os.getenv('SCRATCH'),args.year,args.year,member+1),
        iris.Constraint(time=lambda cell: cell.point.month == args.month)
    )
    pField.coord("latitude").coord_system = coord_s
    pField.coord("longitude").coord_system = coord_s
    pField = pField.collapsed('height',iris.analysis.MEAN)

    # Mean over points where mask==1
    cMean = numpy.mean(pField.data[cGrid.data==1])
    mTMP2m.append(cMean)

# Store the data
cspf = "%s/%04d%02d.pkl" % (args.opdir,args.year,args.month)
pickle.dump(mTMP2m,open(cspf,'wb'))


