#!/usr/bin/bash

# Store the extracted and downloaded 0.0.2 data on MASS

base_dir='/home/h03/hadpb/Projects/20CRv3-diagnostics/tools/extract_data/store_on_mass'

for var in PRMSL PRATE TMP2m TMPS UGRD10m VGRD10m observations
do
for month in {10..12}
do
./v3_scout_to_mass.py --year=1930 --month=$month --version=0.0.2 --variable=$var
done
for month in {1..9}
do
./v3_scout_to_mass.py --year=1931 --month=$month --version=0.0.2 --variable=$var
done
