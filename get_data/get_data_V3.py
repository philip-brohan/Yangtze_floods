#!/usr/bin/env python

# Download the 20CRv3 data for the period around the floods

import IRData.twcr as twcr
import datetime

for year in range(1926, 1936):
    twcr.fetch("observations", datetime.datetime(year, 1, 1), version="3")
    twcr.fetch("PRMSL", datetime.datetime(year, 1, 1), version="3")
    twcr.fetch("PRATE", datetime.datetime(year, 1, 1), version="3")
    twcr.fetch("TMP2m", datetime.datetime(year, 1, 1), version="3")

# Winds only for 1930 and 1931
twcr.fetch("UGRD10m", datetime.datetime(1931, 1, 1), version="3")
twcr.fetch("VGRD10m", datetime.datetime(1931, 1, 1), version="3")
twcr.fetch("UGRD10m", datetime.datetime(1930, 1, 1), version="3")
twcr.fetch("VGRD10m", datetime.datetime(1930, 1, 1), version="3")
