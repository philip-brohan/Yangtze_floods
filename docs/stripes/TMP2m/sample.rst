Get data sample to plot as stripes
==================================

Extracting data for a point in time and making the sampled longitude average is a slow process. So we parallelise it: make one script to make the sample at a given slice in time (day), and then run that script for each day in parallel.

Script to make the sample for one time-slice:

.. literalinclude:: ../../../analyses/stripes_daily/1930s_TMP2m/ensemble/get_slice.py

Script to generate list of time-slices to run:

.. literalinclude:: ../../../analyses/stripes_daily/1930s_TMP2m/ensemble/make_all_slices.py

Library function to make the slice:

.. literalinclude:: ../../../analyses/stripes_daily/1930s_TMP2m/ensemble/get_sample.py


