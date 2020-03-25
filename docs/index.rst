Yangtze Floods of 1931
======================

This document describes a study of the `Yangtze Floods of 1931 <https://en.wikipedia.org/wiki/1931_China_floods>`_ using the `Twentieth Century Reanalysis (20CR) <https://www.esrl.noaa.gov/psd/data/20thC_Rean/>`_ system.

Weather data for 1931
---------------------

The initial aim is to produce a good reanalysis of the weather that caused the flooding. We are looking at three runs of the 20CR system:

* 20CR version 3 (covering 1806-2015)
* Scout run 4.6.1 (covering 1930/10-1931/09). Identical to 20CR version 3 except that it assimilates additional observations from about 40 :doc:`new stations <../new_stations/new_stations>` over China - so it should be more accurate and more precise.
* Scout run 4.6.7 (covering 1930/10-1931/09). Identical to 4.6.1 except for a change to the data assimilation: Data assimilation in 20CR is a compromise between the weather state predicted by the model and the state indicated by the observations. This is necessary to keep the analysis stable, and to cope with errors in both the model formulation and the observations. One tunable parameter in this compromise is the 'relaxation to prior spread' - set universally to 0.9 in 20CR version 3. It would be good to reduce this number, this would allow the observations to produce a bigger reduction in the observation spread, and so a more precise analysis, particularly where observations are infrequent in time (once a day or less often). The risk in doing so is that the reanalysis might become unstable.

.. toctree::
   :maxdepth: 1

   Get data from 20CR version 3 <get_data/get_data_v3>
   Get data from scout 4.6.1 <get_data/get_data_v461>
   Get data from scout 4.6.7 <get_data/get_data_v467>

As well as the reanalysis we would like observations and observational datasets. So far we have a collection of newly-digitised station observations, and the `EUSTACE dataset <https://www.eustaceproject.org/>`_ of daily temperatures.

.. toctree::
   :maxdepth: 1

   Newly-available station data <new_stations/new_stations>
   Get data from EUSTACE <stripes/EUSTACE/data>

Testing the reanalysis runs
---------------------------

One way to quickly judge the quality of the reanalyses for the period in question, is to reproduce the stripes plots, from the `20CRv3 diagnostics <https://oldweather.github.io/20CRv3-diagnostics/index.html>`_, but using daily data just for 1926-1935:

.. toctree::
   :maxdepth: 1

   2m air temperature from EUSTACE <stripes/EUSTACE/index>
   2m air temperature from 20CRv3 <stripes/TMP2m/index>
   2m air temperature: EUSTACE-20CRv3 comparison <stripes/TMP2m+EUSTACE/index>
   2m air temperature: Scout 4.6.1-20CRv3 comparison <stripes/4.6.1_comparison/TMP2m/index>
   2m air temperature: Scout 4.6.7-20CRv3 comparison <stripes/4.6.7_comparison/TMP2m/index>
   Mean-sea-level pressure from 20CRv3 <stripes/PRMSL/index>
   Precipitation rate from 20CRv3 <stripes/PRATE/index>
   
A key question is how successful 20CR is in using pressure observations to reconstruct the weather state over China during the flood period. Is this reconstruction improved by assimilating the :doc:`new station observations <new_stations/new_stations>`? Is it improved by the assimilation parameter changes in scout 4.6.7?

To investigate this, we have made `spaghetti-contour plots <http://brohan.org/offline_assimilation/representing_uncertainty/representing_uncertainty.html>`_ comparing the reanalysis versions:

.. toctree::
   :maxdepth: 1

   MSLP in 20CRv3 compared to scout 4.6.1 <videos/v3_v_v461> 
   MSLP in Scout 4.6.1 compared to scout 4.6.7 <videos/v461_v_v467>

It's clear from the videos that all three reanalysis runs produce plausible mslp reconstructions over China, and that the difference between the runs is modest. It's useful to compare daily time-series of the reconstructed weather for the China region (20-40N, 105-125E):

.. toctree::
   :maxdepth: 1

   Daily MSLP over China <daily_time_series/PRMSL/index> 
   Daily TMP2m over China <daily_time_series/TMP2m/index> 
   Daily Precipitation over China <daily_time_series/PRATE/index> 

These comparisons show that:

* 20CRv3 provides a good reconstruction of the meteorology over China in 1930-1931.
* Assimilating the additional Chinese station observations makes a modest, but noticeable, improvement to the reconstruction - adjusting the ensemble mean to be closer to the observations, and reducing the ensemble spread.
* The assimilation experiment: reducing the 'relaxation to prior spread' from 0.9 to 0.7, is a success - it reduces the ensemble spread without causing any problems.

This set of experiments behaved as we hoped: the initial reconstruction is pretty good, assimilating additional observations improves it, changing the assimilation parameter improves it again. The improvements are modest, but that is because the initial reanalysis (20CRv3) was already good.

Small print
-----------

.. toctree::
   :maxdepth: 1

   Authors and acknowledgements <credits>

This document and the data associated with it, are crown copyright (2020) and distributed under the terms of the `Open Government Licence <https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/>`_. All code included is licensed under the terms of the `GNU Lesser General Public License <https://www.gnu.org/licenses/lgpl.html>`_.
