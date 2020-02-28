#!/usr/bin/bash

# Extract the raw 4.6.7 data for the year of the flood

# This script must be run on Cori

# This script submits jobs to do the data extraction;
#  they take some time to run (days).

base_dir='/global/homes/p/pbrohan/Projects/20CRv3-diagnostics/tools/extract_data/v3_release/'

$base_dir/extract_month_job.py --startyear=1924 --year=1930 --month=10 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1930 --month=11 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1930 --month=12 --version=467

$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=1 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=2 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=3 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=4 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=5 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=6 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=7 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=8 --version=467
$base_dir/extract_month_job.py --startyear=1924 --year=1931 --month=9 --version=467

