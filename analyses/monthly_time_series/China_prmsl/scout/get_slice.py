#!/usr/bin/env python

# 20CRv3 stripes.
# Monthly, mean over lat:lon range, 
#  sampling the ensemble.

# Get the sample for a specified month

import os
import iris
import numpy
import datetime
import pickle

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Month",
                    type=int,required=True)
parser.add_argument("--version", help="Version no (e.g. 4.5.1)",
                    type=str,required=True)
parser.add_argument("--min_lat", help="Min latitude",
                    type=float,required=False,default=-90.0)
parser.add_argument("--max_lat", help="Max latitude",
                    type=float,required=False,default=90.0)
parser.add_argument("--min_lon", help="Min longitude",
                    type=float,required=False,default=-180.0)
parser.add_argument("--max_lon", help="Max longitude",
                    type=float,required=False,default=360.0)
parser.add_argument("--opdir", help="Directory for output files",
                    default="analyses/Yangtze_ts/PRMSL",
                    type=str,required=False)
args = parser.parse_args()
args.opdir = "%s/20CR/version_%s/%s" % (os.getenv('SCRATCH'),args.version,args.opdir)
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

# Fix dask SPICE bug
import dask
dask.config.set(scheduler='single-threaded')

from get_sample import get_sample

cpkl="%s/20CR/version_3/monthly_means/PRMSL.climatology.1926-35.pkl" % os.getenv('SCRATCH')
climatology=pickle.load(open(cpkl,'rb'))

ndata = get_sample(max_lat=args.max_lat,
                              min_lat=args.min_lat,
                              max_lon=args.max_lon,
                              min_lon=args.min_lon,
                              year=args.year,
                              month=args.month,
                              climatology=climatology,
                              version=args.version)

cspf = "%s/%04d%02d.pkl" % (args.opdir,args.year,args.month)
pickle.dump(ndata,open(cspf,'wb'))
   
