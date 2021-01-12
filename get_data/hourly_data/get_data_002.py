#!/usr/bin/env python

# Download the scout 0.0.2 data for the year of the flood

# Do the data extraction on Cori before running these retrievals

# Set up the NERSC ssh proxy before running these retrievals
#  ~/bin/sshproxy.sh -u pbrohan
# Otherwise each retrieval will request a password

import IRData.twcr as twcr
import datetime

for month in (10, 11, 12):
    try:
        twcr.fetch("observations", datetime.datetime(1930, month, 1), version="0.0.2")
        twcr.fetch("PRMSL", datetime.datetime(1930, month, 1), version="0.0.2")
        twcr.fetch("PRATE", datetime.datetime(1930, month, 1), version="0.0.2")
        twcr.fetch("TMP2m", datetime.datetime(1930, month, 1), version="0.0.2")
        twcr.fetch("TMPS", datetime.datetime(1930, month, 1), version="0.0.2")
        twcr.fetch("UGRND10m", datetime.datetime(1930, month, 1), version="0.0.2")
        twcr.fetch("VGRND10m", datetime.datetime(1930, month, 1), version="0.0.2")
    except:
        print("Failed retrieval for 1930-%02" % month)

for month in (1, 2, 3, 4, 5, 6, 7, 8, 9):
    try:
        twcr.fetch("observations", datetime.datetime(1931, month, 1), version="0.0.2")
        twcr.fetch("PRMSL", datetime.datetime(1931, month, 1), version="0.0.2")
        twcr.fetch("PRATE", datetime.datetime(1931, month, 1), version="0.0.2")
        twcr.fetch("TMP2m", datetime.datetime(1931, month, 1), version="0.0.2")
        twcr.fetch("TMPS", datetime.datetime(1931, month, 1), version="0.0.2")
        twcr.fetch("UGRND10m", datetime.datetime(1931, month, 1), version="0.0.2")
        twcr.fetch("VGRND10m", datetime.datetime(1931, month, 1), version="0.0.2")
    except Exception:
        print("Failed retrieval for 1931-%02" % month)
