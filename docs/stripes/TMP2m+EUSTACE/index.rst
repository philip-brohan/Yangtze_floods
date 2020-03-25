EUSTACE-20CRv3 TMP2m daily stripes for 1926-1935
================================================

.. figure:: ../../../analyses/stripes_daily/1930s_TMP2m+EUSTACE/ensemble/comparison_grid.png
   :width: 95%
   :align: center
   :figwidth: 95%

   Daily 2m-temperature anomalies (w.r.t. 1926-35) from the EUSTACE ensemble (top), the 20CRv3 ensemble (middle), and the difference between the two (bottom). The vertical axis is latitude, and each pixel is a longitudinal mean from a randomly selected ensemble member. For latitude:time points (pixels) where data are missing for some longitudes, the pixel is either the average of all available longitude points, or shown as missing - this decision is made at random, the probability of being missing is equal to the fraction of missing longitude points.

Sampling in this way means that regions where the variance across the ensemble is large, or where much of the data is missing, appear speckled. This provides an indication of uncertainty.

.. toctree::
   :titlesonly:
   :maxdepth: 1

   Scripts to make the EUSTACE data <../EUSTACE/index.rst>
   Scripts to make the 20CRv3 data <../TMP2m/index.rst>
   Scripts to make the plot <./plot.rst>
   Function to extract the comparison data sample <./sample.rst>
