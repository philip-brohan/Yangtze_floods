#!/bin/bash

# Make all the timeseries plots for the Yangtze catchment

for var in PRMSL PRATE TMP2m PWAT WEASD
do
    ./decadal_values_over_catchment.py --version=3 --var=$var | spice_parallel --time=10 --batch=3
    ./decadal_values_over_catchment.py --version=3 --var=$var | spice_parallel --time=10 --batch=1
    ./all_values_over_catchment.py --version=0.0.2 --var=$var | spice_parallel --time=10 --batch=3
    ./all_values_over_catchment.py --version=0.0.2 --var=$var | spice_parallel --time=10 --batch=1
    ./all_values_over_catchment.py --version=4.6.1 --var=$var | spice_parallel --time=10 --batch=3
    ./all_values_over_catchment.py --version=4.6.1 --var=$var | spice_parallel --time=10 --batch=1
done

./plot_ts_full.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PRMSL --yscale=0.01
./plot_ts_full_anomaly.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PRMSL --yscale=0.01

./plot_ts_full.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PRATE --yscale=1000

./plot_ts_full.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=TMP2m
./plot_ts_full_anomaly.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=TMP2m

./plot_ts_full.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PWAT
./plot_ts_full_anomaly.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PWAT

./plot_ts_full.py --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=WEASD --ymax=25
