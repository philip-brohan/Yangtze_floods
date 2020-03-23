Make daily PRMSL climatology over 1926-1935
===========================================

Extracting data for a day and making the time average is a slow process. So we parallelise it: make one script to make the sample at a given slice in time (day), and then run that script for each day in parallel.

Script to make the climatology for one day:

.. literalinclude:: ../../../analyses/stripes_daily/1930s_PRMSL/ensemble/make_climatology_for_day.py

Script to generate list of days to run:

.. literalinclude:: ../../../analyses/stripes_daily/1930s_PRMSL/ensemble/make_all_climatology_days.py

Library function to make the slice:

.. literalinclude:: ../../../analyses/stripes_daily/1930s_PRMSL/ensemble/get_sample.py


