#!/usr/bin/env python

# 20CRv3 stripes.
# Daily, mean over lat:lon range, 
#  sampling the ensemble.

# Get the sample for a specified day

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
parser.add_argument("--day", help="Day",
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
                    default="analyses/Yangtze_ts_daily/PRATE",
                    type=str,required=False)
args = parser.parse_args()
args.opdir = "%s/20CR/version_%s/%s" % (os.getenv('SCRATCH'),args.version,args.opdir)
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

# Fix dask SPICE bug
import dask
dask.config.set(scheduler='single-threaded')

from get_sample import get_sample

cdy = args.day
if args.month==2 and args.day==29: cdy=28
cpkl="%s/20CR/version_3/analyses/daily/PRATE/clim_1926-1935/%02d%02d.pkl" % (
           os.getenv('SCRATCH'),args.month,cdy)
climatology=pickle.load(open(cpkl,'rb'))

ndata = get_sample(max_lat=args.max_lat,
                              min_lat=args.min_lat,
                              max_lon=args.max_lon,
                              min_lon=args.min_lon,
                              year=args.year,
                              month=args.month,
                              day=args.day,
                              climatology=climatology,
                              version=args.version)

cspf = "%s/%04d%02d%02d.pkl" % (args.opdir,args.year,args.month,args.day)
pickle.dump(ndata,open(cspf,'wb'))
   
