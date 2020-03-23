TMP2m over China: Daily time-series for 1930-1931
=================================================

.. figure:: ../../../analyses/daily_time_series/China_TMP2m/TMP2m_ts.png
   :width: 95%
   :align: center
   :figwidth: 95%

   Daily 2m air temperature anomalies (w.r.t. 1926-35) over China (20-40N, 105-125E) from the 20CRv3 ensemble (in black) and the scout runs 4.6.1 (in blue - offset by +4c) and 4.6.7 (in red - offset by -4C). In each case 80 lines are plotted - one for each ensemble member. 

.. toctree::
   :titlesonly:
   :maxdepth: 1

   Scripts to make the 1926-35 climatology <../../stripes/TMP2m/climatology.rst>
   Scripts to make the plot <./plot.rst>
   Function to extract the data sample <./sample.rst>

The three series are very similar; to see the effect of the changes in the scout runs it's useful to also plot the difference between them.

.. figure:: ../../../analyses/daily_time_series/China_TMP2m/TMP2m_dts_s.png
   :width: 95%
   :align: center
   :figwidth: 95%

   Bottom panel: as above, except anomaly w.r.t the 20CRv3 ensemble mean for the day. Top panel, the ensemble spread, for each reanalysis run, for each day.

.. toctree::
   :titlesonly:
   :maxdepth: 1

   Scripts to make the difference plot <./plot_dts.rst>
