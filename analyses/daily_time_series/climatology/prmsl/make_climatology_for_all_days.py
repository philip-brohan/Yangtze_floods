#!/usr/bin/env python

# Make the daily climatology for all days in the year

import datetime
import os

current=datetime.date(1926,1,1)
while current.year==1926:

   opf="%s/20CR/version_3/daily_means/PRMSL.climatology.1926-35/%02d%02d.pkl" % (
                os.getenv('SCRATCH'),current.month,current.day)

   if not os.path.exists(opf):
       print("./make_climatology_for_day.py --month=%d --day=%d" % (
                  current.month,current.day))

   current += datetime.timedelta(days=1)
