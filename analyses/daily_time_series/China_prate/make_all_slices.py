#!/usr/bin/env python

# Scripts to make slices for every month

import os
from calendar import monthrange

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--version", help="Run number, e.g. 4.5.1",
                    type=str,required=True)
parser.add_argument("--min_lat", help="Min latitude",
                    type=float,required=False,default=20)
parser.add_argument("--max_lat", help="Max latitude",
                    type=float,required=False,default=40.0)
parser.add_argument("--min_lon", help="Min longitude",
                    type=float,required=False,default=105)
parser.add_argument("--max_lon", help="Max longitude",
                    type=float,required=False,default=125.0)
args = parser.parse_args()

for year in range(1929,1933):
    for month in range (1,13):

        if args.version=='3':
            if year == 1929 and month <10: continue
            if year == 1932 and month >9:  continue
        else:
            if year < 1930 or year > 1931: continue
            if year == 1930 and month <10: continue
            if year == 1931 and month >9:  continue

        for day in range(1,monthrange(year,month)[1]+1):

            opf="%s/20CR/version_%s/analyses/Yangtze_ts_daily/PRATE/%04d%02d%02d.pkl" % (
                   os.getenv('SCRATCH'),args.version,year,month,day)
            if os.path.exists(opf):
                continue

            print(("./get_slice.py --year=%d "+
                   "--month=%d --day=%d --version=%s "+
                   "--min_lat=%f --max_lat=%f "+
                   "--min_lon=%f --max_lon=%f") % (
                    year,month,day,args.version,
                    args.min_lat,args.max_lat,
                    args.min_lon,args.max_lon))
