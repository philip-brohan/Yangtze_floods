#!/usr/bin/env python

# Download the scout 0.0.2 data for the year of the flood

# Do the data extraction on Cori before running these retrievals

# Set up the NERSC ssh proxy before running these retrievals
#  ~/bin/sshproxy.sh -u pbrohan
# Otherwise each retrieval will request a password

import IRData.twcr as twcr
import datetime

for month in (10, 11, 12):
    for var in ("observations","PRMSL","PRATE","TMP2m","TMPS","PWAT","WEASD","UGRND10m","VGRND10m"):
        try:
            twcr.fetch(var, datetime.datetime(1930, month, 1), version="0.0.1")
        except:
            print("Failed %s retrieval for 1930-%02d" % (var,month))

for month in (1, 2, 3, 4, 5, 6, 7, 8, 9):
    for var in ("observations","PRMSL","PRATE","TMP2m","TMPS","PWAT","WEASD","UGRND10m","VGRND10m"):
        try:
            twcr.fetch(var, datetime.datetime(1931, month, 1), version="0.0.1")
        except:
            print("Failed %s retrieval for 1931-%02d" % (var,month))
