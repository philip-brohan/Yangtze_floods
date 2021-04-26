#!/usr/bin/bash

# Fetch the extracted and downloaded 0.0.2 data from MASS

base_dir='/home/h03/hadpb/Projects/20CRv3-diagnostics/tools/extract_data/store_on_mass'

$base_dir/v3_scout_from_mass.py --year=1930 --month=10 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1930 --month=11 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1930 --month=12 --version=0.0.2 --variable=all

$base_dir/v3_scout_from_mass.py --year=1931 --month=1 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=2 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=3 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=4 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=5 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=6 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=7 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=8 --version=0.0.2 --variable=all
$base_dir/v3_scout_from_mass.py --year=1931 --month=9 --version=0.0.2 --variable=all
