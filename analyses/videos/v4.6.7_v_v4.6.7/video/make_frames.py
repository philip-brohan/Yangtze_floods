#!/usr/bin/env python

# Make all the individual frames for a movie
#  run the jobs on SPICE.

import os
import datetime

# Where to put the output files
opdir="%s/images/Yangtze_1931_v4.6.1_v_4.6.7" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this timepoint
def is_done(dte):
    op_file_name=('%s/%04d%02d%02d%02d%02d.png' % 
                             (opdir,dte.year,dte.month,dte.day,
                              int(dte.hour),int(dte.hour%1*60)))
    if os.path.isfile(op_file_name):
        return True
    return False

start_day=datetime.datetime(1930, 10,  1,  3)
end_day  =datetime.datetime(1930, 10, 31, 21)

dte=start_day
while dte<=end_day:
    if not is_done(dte):
        cmd="./plot_comparison.py --year=%d --month=%d --day=%d --hour=%f" % (
                       dte.year,dte.month,dte.day,
                       dte.hour+dte.minute/60)
        print(cmd)
    dte=dte+datetime.timedelta(minutes=15)
