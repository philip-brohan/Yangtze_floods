#!/usr/bin/env python

# Scripts to make slices for every month

import os
import datetime
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--version", help="Run number, e.g. 4.5.1",
                    type=str,required=True)
parser.add_argument("--min_lat", help="Min latitude",
                    type=float,required=False,default=20)
parser.add_argument("--max_lat", help="Max latitude",
                    type=float,required=False,default=50.0)
parser.add_argument("--min_lon", help="Min longitude",
                    type=float,required=False,default=70)
parser.add_argument("--max_lon", help="Max longitude",
                    type=float,required=False,default=130.0)
args = parser.parse_args()

for year in (1930,1931):
    for month in range (1,13):

        if year == 1930 and month <10: continue
        if year == 1931 and month >9:  continue

        opf="%s/20CR/version_%s/analyses/Yangtze_ts/PRMSL/%04d%02d.pkl" % (
               os.getenv('SCRATCH'),args.version,year,month)
        if os.path.exists(opf):
            continue

        print(("./get_slice.py --year=%d "+
               "--month=%d --version=%s "+
               "--min_lat=%f --max_lat=%f "+
               "--min_lon=%f --max_lon=%f") % (
                year,month,args.version,
                args.min_lat,args.max_lat,
                args.min_lon,args.max_lon))
