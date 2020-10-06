#!/usr/bin/env python

# Retrieve 20CRv3 monthly ensembles from NERSC

import sys
import os
import subprocess
import os.path
import glob
import tarfile

# What to retrieve
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument(
    "--variable", help="Variable name ('PRMSL', 'PRATE',...)", type=str, required=True
)
args = parser.parse_args()

# Base location at NERSC
nersc = (
    "https://portal.nersc.gov/archive/home/projects/incite11/"
    + "www/20C_Reanalysis_version_3/everymember_anal_netcdf/mnmean"
)

# Disc data dir
ddir = "%s/20CR/version_3/monthly/" % os.environ["SCRATCH"]
if not os.path.isdir(ddir):
    os.makedirs(ddir)

# Already done?
ofiles = glob.glob(
    "%s/%04d/%s.%04d.mnmean_mem*.nc" % (ddir, args.year, args.variable, args.year)
)
if len(ofiles) > 79:
    sys.exit(0)  # Already on disc

# download the tar file
cmd = "wget -O %s/%s_%04d_mnmean.tar %s/%s/%s_%04d_mnmean.tar" % (
    ddir,
    args.variable,
    args.year,
    nersc,
    args.variable,
    args.variable,
    args.year,
)
wg_retvalue = subprocess.call(cmd, shell=True)
if wg_retvalue != 0:
    raise Exception("Failed to download data")

# Unpack the by-member nc files
tar = tarfile.open("%s/%s_%04d_mnmean.tar" % (ddir, args.variable, args.year), "r")
tar.extractall(path=ddir)
tar.close()

# Reset the modification time -
#     otherwise scratch will delete them.
ofiles = glob.glob(
    "%s/%04d/%s.%04d.mnmean_mem*.nc" % (ddir, args.year, args.variable, args.year)
)
for ofile in ofiles:
    os.utime(ofile, None)
