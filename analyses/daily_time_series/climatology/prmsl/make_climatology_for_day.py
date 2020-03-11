#!/usr/bin/env python

# Make daily climatology from 20CRv3

import os
import iris
import IRData.twcr as twcr
import numpy
import datetime
import pickle

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--month", help="Month",
                    type=int,required=True)
parser.add_argument("--day", help="Day",
                    type=int,required=True)
args = parser.parse_args()

cpkl="%s/20CR/version_3/daily_means/PRMSL.climatology.1926-35/%02d%02d.pkl" % (
                os.getenv('SCRATCH'),args.month,args.day)

opdir = os.path.dirname(cpkl)
if not os.path.isdir(opdir):
    os.makedirs(opdir)

def load_daily_v3(year,month,day):
    e=[]
    for member in range(1,81):
         f=iris.load_cube('%s/20CR/version_3/%04d/PRMSL.%04d_mem%03d.nc' % 
                                                           (os.getenv('SCRATCH'),year,year,member),
                             iris.Constraint(name='Pressure reduced to MSL') &
                             iris.Constraint(time=lambda cell: \
                                             cell.point.year == year and \
                                             cell.point.month == month and \
                                             cell.point.day == day))
         f=f.collapsed('time', iris.analysis.MEAN)
         f.attributes=None
         f.add_aux_coord(iris.coords.AuxCoord(member, long_name='member'))         
         e.append(f)
    e=iris.cube.CubeList(e).merge_cube()
    return(e)

e=[]
for year in range(1926,1936):
    h=load_daily_v3(year,args.month,args.day)
    h=h.collapsed('member', iris.analysis.MEAN)
    e.append(h)
e=iris.cube.CubeList(e).merge_cube()
e=e.collapsed('time', iris.analysis.MEAN)
    
pickle.dump(e,open(cpkl,'wb'))

