# Get the sample cube for 20CR
# Sample in the ensemble.
# Resolved in latitude, average in longitude.

import os
import iris
import IRData.twcr as twcr
import numpy
import datetime
from calendar import monthrange
from iris.experimental.equalise_cubes import equalise_attributes
import sys
import pickle

def load_daily_scout(year,month,day,version):
    e=[]
    for hour in (0,3,6,9,12,15,18,21):
         f=twcr.load('prate',datetime.datetime(year,month,day,hour),version=version)
         e.append(f)
    e=iris.cube.CubeList(e).merge_cube()
    e=e.collapsed('time', iris.analysis.MEAN)
    return(e)

def load_daily_v3(year,month,day):
    e=[]
    for member in range(1,81):
         f=iris.load_cube('%s/20CR/version_3/%04d/PRATE.%04d_mem%03d.nc' % 
                                                           (os.getenv('SCRATCH'),year,year,member),
                             iris.Constraint(name='Precipitation rate') &
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

def load_daily(year,month,day,version='3'):
    if version=='3':
        return load_daily_v3(year,month,day)
    else:
        return load_daily_scout(year,month,day,version)


def get_sample(min_lon=-180,max_lon=360,min_lat=-90,max_lat=90,
               year=None,month=None,day=None,
               climatology=None,
               version=3,
               new_grid=None):

    # Load the model data
    m=load_daily(year,month,day,version=version)

    # Anomalise
    if climatology is not None:
        m.data -= climatology.data

    if new_grid is not None:
        m = m.regrid(new_grid,iris.analysis.Nearest())

    # Reduce to area of interest
    m.coord('latitude').guess_bounds()
    m.coord('longitude').guess_bounds()
    m=m.extract(iris.Constraint(longitude=lambda v: min_lon <= v <= max_lon,
                                latitude =lambda v: min_lat <= v <= max_lat))

            
    # Get area averages
    w = iris.analysis.cartography.area_weights(m)
    ndata=numpy.ma.array(numpy.zeros((1,80)),mask=True)
    ndata[0,:]=m.collapsed(['latitude', 'longitude'],
                           iris.analysis.MEAN,
                           weights=w).data
    return ndata

