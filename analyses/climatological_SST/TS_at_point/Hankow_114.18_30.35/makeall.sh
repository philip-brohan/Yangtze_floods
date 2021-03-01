#!/bin/bash

# Make all the timeseries plots for Hankow.

export lat='30.35'
export lon='114.18'

for var in PRMSL PRATE TMP2m PWAT WEASD
do
    ../decadal_values_at_point.py --lat=$lat --lon=$lon --version=3 --var=$var | spice_parallel --time=10 --batch=3
    ../decadal_values_at_point.py --lat=$lat --lon=$lon --version=3 --var=$var | spice_parallel --time=10 --batch=1
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=0.0.2 --var=$var | spice_parallel --time=10 --batch=3
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=0.0.2 --var=$var | spice_parallel --time=10 --batch=1
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.1 --var=$var | spice_parallel --time=10 --batch=3
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.1 --var=$var | spice_parallel --time=10 --batch=1
done

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PRMSL --yscale=0.01
../plot_ts_full_anomaly.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PRMSL --yscale=0.01

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PRATE --yscale=1000 --ymax=1.0

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=TMP2m
../plot_ts_full_anomaly.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=TMP2m

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PWAT
../plot_ts_full_anomaly.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=PWAT

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison=0.0.2 --comparison2=4.6.1 --var=WEASD --ymax=35
