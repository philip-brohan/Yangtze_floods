#!/usr/bin/env python

# Get the PRMSL over the Yangtze catchment for all the months we need.
#  (Strictly, just assemble a list of commands to run to do this).

# Years of interest
for year in range(1920,1941):
    for month in range(1,13):
        print("./get_value_for_month.py --year=%d --month=%d" % (year,month))

# Climatology years
for year in range(1961,1991):
    for month in range(1,13):
        print("./get_value_for_month.py --year=%d --month=%d" % (year,month))
