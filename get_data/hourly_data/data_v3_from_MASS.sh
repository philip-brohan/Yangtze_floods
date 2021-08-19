#!/usr/bin/bash

# Fetch the extracted and downloaded v3 data from MASS

base_dir='/home/h03/hadpb/Projects/20CRv3-diagnostics/tools/extract_data/store_on_mass'

for year in {1926..1935}
do
for var in observations PRMSL PRATE PWAT TMP2m TMPS WEASD
do
$base_dir/v3_release_from_mass.py --year=$year --variable=$var
done
done
