Download data from 20CRv3
=========================

20CRv3 reanalysis output is distributed through `a web portal at NERSC <https://portal.nersc.gov/project/20C_Reanalysis/>`_. It is straightforward to download it, but note that the data volume is large (about 40Gb for one 2d variable - e.g. TMP2m - for one year) and the data is kept on tape at NERSC so it can take some time to download.

Script to download the data (uses the `IRData library <http://brohan.org/IRData/>`_):

.. literalinclude:: ../../get_data/get_data_V3.py
