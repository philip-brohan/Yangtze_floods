Download data from scout 4.6.1
==============================

Getting data from 20CR scout runs is much more complex than :doc:`getting it from the released version <get_data_v3>`. Scout runs are not postprocessed or distributed, so you need to log on to `Cori <https://docs.nersc.gov/systems/cori/>`_ and extract the data yourself.

Instructions (and code) for scout run data extraction are `available here <https://oldweather.github.io/20CRv3-diagnostics/extract_data/extract_data.html>`_.

Script to extract the data used here (must be run on `Cori <https://docs.nersc.gov/systems/cori/>`_):

.. literalinclude:: ../../get_data/extract_data_461.sh

When this data extraction is complete, download the data to your local system.

Script to download the data (uses the `IRData library <http://brohan.org/IRData/>`_):

.. literalinclude:: ../../get_data/get_data_461.py
