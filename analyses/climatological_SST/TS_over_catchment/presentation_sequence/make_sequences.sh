#!/usr/bin/bash

# Make sets of time-series figures for use in presentations

../plot_ts_full.py --opfile=tst.png --var=PRATE --yscale=1000 --climatology --opfile=PRATE_climatology.png

../plot_ts_full.py --opfile=tst.png --var=PRATE --yscale=1000 --climatology --interannual --opfile=PRATE_interannual.png

../plot_ts_full.py --opfile=tst.png --var=PRATE --yscale=1000 --climatology --interannual --mean --opfile=PRATE_mean.png

../plot_ts_full.py --opfile=tst.png --var=PRATE --yscale=1000 --climatology --interannual --mean --ensemble --opfile=PRATE_ensemble.png

../plot_ts_full.py --opfile=tst.png --var=PRATE --yscale=1000 --climatology --interannual --mean --ensemble --comparison=0.0.1 --opfile=PRATE_comparison.png

../plot_ts_full.py --opfile=tst.png --var=TMP2m --climatology --opfile=TMP2m_climatology.png

../plot_ts_full.py --opfile=tst.png --var=TMP2m --climatology --interannual --opfile=TMP2m_interannual.png

../plot_ts_full.py --opfile=tst.png --var=TMP2m --climatology --interannual --mean --opfile=TMP2m_mean.png

../plot_ts_full.py --opfile=tst.png --var=TMP2m --climatology --interannual --mean --ensemble --opfile=TMP2m_ensemble.png

../plot_ts_full.py --opfile=tst.png --var=TMP2m --climatology --interannual --mean --ensemble --comparison=0.0.1 --opfile=TMP2m_comparison.png

../plot_ts_full_anomaly.py --version=3 --comparison=0.0.1 --var=TMP2m --opfile=TMP2m_anomaly_comparison.png

../plot_ts_full_anomaly.py --version=3  --var=TMP2m --opfile=TMP2m_anomaly.png

../plot_ts_full.py --opfile=tst.png --var=PWAT --climatology --opfile=PWAT_climatology.png

../plot_ts_full.py --opfile=tst.png --var=PWAT --climatology --interannual --opfile=PWAT_interannual.png

../plot_ts_full.py --opfile=tst.png --var=PWAT --climatology --interannual --mean --opfile=PWAT_mean.png

../plot_ts_full.py --opfile=tst.png --var=PWAT --climatology --interannual --mean --ensemble --opfile=PWAT_ensemble.png

../plot_ts_full.py --opfile=tst.png --var=PWAT --climatology --interannual --mean --ensemble --comparison=0.0.1 --opfile=PWAT_comparison.png
