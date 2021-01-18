#!/usr/bin/env python

import datetime
import os

start = datetime.datetime(1930, 10, 1, 6)
end = datetime.datetime(1931, 9, 30, 18)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--var", help="Variable to extract", type=str, required=True)
parser.add_argument(
    "--version",
    help="20CR version ('3' or e.g. '4.6.5')",
    type=str,
    required=True,
)
args = parser.parse_args()

current = start
while current < end:
    opfile = "%s/20CRv3_Yangtze_data/version_%s/%s/%04d/%02d/%02d/%02d_00.pkl" % (
        os.getenv("SCRATCH"),
        args.version,
        args.var,
        current.year,
        current.month,
        current.day,
        current.hour,
    )
    if not os.path.isfile(opfile):
        print(
            (
                "./store_20CR_Yangtze_catchment_average.py --version=%s --year=%d"
                + " --month=%d --day=%d --hour=%d --var=%s"
            )
            % (
                args.version,
                current.year,
                current.month,
                current.day,
                current.hour,
                args.var,
            )
        )
    current += datetime.timedelta(hours=3)
