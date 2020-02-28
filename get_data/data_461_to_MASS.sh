#!/usr/bin/bash

# Store the extracted and downloaded 4.6.7 data on MASS

base_dir='/home/h03/hadpb/Projects/20CRv3-diagnostics/tools/extract_data/store_on_mass'

$base_dir/v3_to_mass.py --year=1930 --month=10 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=11 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=12 --version=4.6.1 --variable=all

$base_dir/v3_to_mass.py --year=1930 --month=1 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=2 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=3 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=4 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=5 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=6 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=7 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=8 --version=4.6.1 --variable=all
$base_dir/v3_to_mass.py --year=1930 --month=9 --version=4.6.1 --variable=all
