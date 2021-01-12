#!/usr/bin/bash

# Extract the raw 0.0.2 data for the year of the flood

# This script must be run on Cori, using the 20CRv3 conda environment

base_dir='/global/homes/p/pbrohan/Projects/20CRv3-diagnostics/tools/extract_data/scout_ncdf_monthly'

for month in {10..12}
do
$base_dir/month_from_tape.py --startyear=1924 --year=1930 --month=$month --version=002
$base_dir/month_from_tape.py --startyear=1924 --year=1930 --month=$month --version=002
done

for month in {1..9}
do
$base_dir/month_from_tape.py --startyear=1924 --year=1931 --month=$month --version=002
$base_dir/month_from_tape.py --startyear=1924 --year=1931 --month=$month --version=002
done

