Additional observations from Chinese weather stations
=====================================================

20CR version 3 had very few observations from Chinese weather stations, available to assimilate, before about 1950. (See the `observations coverage video <https://vimeo.com/364280156>`_). Participants in ACRE-China have been working to provide additional observations: `Beijing Climate Centre <http://bcc.ncc-cma.net/>`_ have provided digitised pressures from six long station series, and the Met Office Hadley Centre have been transcribing observations from the `China Coast Meteorological Register <https://catalog.hathitrust.org/Record/100620384>`_. The 20CR team have converted these newly-available observations into standard formats and used them in reanalysis scout runs.

These observations will eventually be available as part of `GLAMOD <https://climate.copernicus.eu/global-land-and-marine-observations-database-0>`_. For the moment, they are on-line `here <https://drive.google.com/drive/folders/1kQJkMWmq0Et10qEO-HLAS0ZWgDldNExc>`_, in `SEF format <https://github.com/C3S-Data-Rescue-Lot1-WP3/SEF/wiki>`_.

.. figure:: ../../analyses/new_stations/stations.png
   :width: 75%
   :align: center
   :figwidth: 75%

   Names and locations of the new stations.

|

* :download:`Data file with station names and locations<../../analyses/new_stations/new_stations>`. (Taken from the reanalysis observations feedback output).

Script to read the data file:

.. literalinclude:: ../../analyses/new_stations/new_stations.py

Script to make the figure:

.. literalinclude:: ../../analyses/new_stations/plot_stations.py

