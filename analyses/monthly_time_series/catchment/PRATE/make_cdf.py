#!/usr/bin/env python

# Calculate the Cumulative Distribution Function (cdf) of the Yangtze PRATE anomaly
#  monthly timeseries.

# Uses pre-calculated time-series.

import os
import numpy
import pickle

opdir="%s/20CR/version_3/analyses/Yangtze_catchment_ts/PRATE" % os.getenv('SCRATCH')

# Make the climatology
clim = []
for month in range(1,13):
    mClim=0
    for year in range(1961,1991):
        cspf = "%s/%04d%02d.pkl" % (opdir,year,month)
        with open( cspf, "rb" ) as pfile:
            mtmp= pickle.load(pfile)
            mClim += sum(mtmp)/len(mtmp)
    clim.append(mClim/30)
    
# Make the anomaly quantiles
tSeries = []
for year in range(1850,2015):
    for month in range(1,13):
        cspf = "%s/%04d%02d.pkl" % (opdir,year,month)
        with open( cspf, "rb" ) as pfile:
            mtmp= pickle.load(pfile)
        for member in range(len(mtmp)):
            tSeries.append((mtmp[member]-clim[month-1]))

qts = numpy.quantile(tSeries,numpy.arange(0.001,0.9999,0.001))

# Store the data
cspf = "%s/anomaly_quantiles.pkl" % opdir
pickle.dump(qts,open(cspf,'wb'))



