#!/usr/bin/env python

# Download the scout 4.6.1 data for the year of the flood

# Do the data extraction on Cori before running these retrievals

# Set up the NERSC ssh proxy before running these retrievals
#  ~/bin/sshproxy.sh -u pbrohan
# Otherwise each retrieval will request a password

import IRData.twcr as twcr
import datetime

for month in (10, 11, 12):
    try:
        twcr.fetch("observations", datetime.datetime(1930, month, 1), version="4.6.1")
        twcr.fetch("prmsl", datetime.datetime(1930, month, 1), version="4.6.1")
        twcr.fetch("prate", datetime.datetime(1930, month, 1), version="4.6.1")
        twcr.fetch("tmp", datetime.datetime(1930, month, 1), height=2, version="4.6.1")
        twcr.fetch("uwnd.10m", datetime.datetime(1930, month, 1), version="4.6.1")
        twcr.fetch("vwnd.10m", datetime.datetime(1930, month, 1), version="4.6.1")
    except Exception:
        print("Failed retrieval for 1930-%02" % month)

for month in (1, 2, 3, 4, 5, 6, 7, 8, 9):
    try:
        twcr.fetch("observations", datetime.datetime(1931, month, 1), version="4.6.1")
        twcr.fetch("prmsl", datetime.datetime(1931, month, 1), version="4.6.1")
        twcr.fetch("prate", datetime.datetime(1931, month, 1), version="4.6.1")
        twcr.fetch("tmp", datetime.datetime(1931, month, 1), height=2, version="4.6.1")
        twcr.fetch("uwnd.10m", datetime.datetime(1931, month, 1), version="4.6.1")
        twcr.fetch("vwnd.10m", datetime.datetime(1931, month, 1), version="4.6.1")
    except Exception:
        print("Failed retrieval for 1931-%02" % month)
