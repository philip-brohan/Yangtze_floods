Get scout 4.6.7 data sample to plot as stripes
==============================================

Extracting data for a point in time and making the sampled longitude average is a slow process. So we parallelise it: make one script to make the sample at a given slice in time (day), and then run that script for each day in parallel.

Script to make the sample for one time-slice:

.. literalinclude:: ../../../../analyses/stripes_daily/4.6.7_comparison/1930s_TMP2m/ensemble/get_slice_467.py

Script to generate list of time-slices to run (only for 1 year - that's all the data we have for 4.6.7):

.. literalinclude:: ../../../../analyses/stripes_daily/4.6.7_comparison/1930s_TMP2m/ensemble/make_all_slices_467.py

Library function to make the slice:

.. literalinclude:: ../../../../analyses/stripes_daily/4.6.7_comparison/1930s_TMP2m/ensemble/get_sample_467.py


