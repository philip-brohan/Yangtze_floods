Get data sample to plot as time-series
======================================

Extracting a regional average for all ensemble members is a slow process. So we parallelise it: make one script to make the averages at a given slice in time (day), and then run that script for each day in parallel.

Script to make the averages for one day:

.. literalinclude:: ../../../analyses/daily_time_series/China_TMP2m/get_slice.py

Script to generate list of time-slices to run:

.. literalinclude:: ../../../analyses/daily_time_series/China_TMP2m/make_all_slices.py

Library function to make the sample:

.. literalinclude:: ../../../analyses/daily_time_series/China_TMP2m/get_sample.py


