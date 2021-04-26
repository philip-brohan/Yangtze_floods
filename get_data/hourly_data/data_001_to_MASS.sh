#!/usr/bin/bash

# Store the extracted and downloaded 0.0.1 data on MASS

base_dir='/home/h03/hadpb/Projects/20CRv3-diagnostics/tools/extract_data/store_on_mass'

for var in PRMSL PRATE TMP2m TMPS UGRD10m VGRD10m observations
do
for month in {10..12}
do
$base_dir/v3_scout_to_mass.py --year=1930 --month=$month --version=0.0.1 --variable=$var
done
for month in {1..7}
do
$base_dir/v3_scout_to_mass.py --year=1931 --month=$month --version=0.0.1 --variable=$var
done
done

