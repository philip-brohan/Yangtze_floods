#!/bin/bash

for i in `seq 1850 2016`;
do
./get_20CRv3_monthly.py --year=$i --variable=PRMSL
./get_20CRv3_monthly.py --year=$i --variable=PRATE
./get_20CRv3_monthly.py --year=$i --variable=TMP2m
./get_20CRv3_monthly.py --year=$i --variable=TMPS
done    
        
