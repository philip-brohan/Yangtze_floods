#!/usr/bin/env python

# Get the PRMSL over the Yangtze catchment for all the months we need.
#  (Strictly, just assemble a list of commands to run to do this).

import os

def done(year,month):
    if os.path.exists("%s/20CR/version_3/analyses/Yangtze_catchment_ts/PRATE/%04d%02d.pkl" % (os.getenv('SCRATCH'),year,month)): return True
    return False


# Years of interest
for year in range(1850,2016):
    for month in range(1,13):
        if done(year,month):
            continue
        print("./get_value_for_month.py --year=%d --month=%d" % (year,month))

# Climatology years
#for year in range(1961,1991):
#    for month in range(1,13):
#        if done(year,month):
#            continue
#        print("./get_value_for_month.py --year=%d --month=%d" % (year,month))
