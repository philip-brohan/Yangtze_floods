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
         f=twcr.load('prmsl',datetime.datetime(year,month,day,hour),version=version)
         e.append(f)
    e=iris.cube.CubeList(e).merge_cube()
    e=e.collapsed('time', iris.analysis.MEAN)
    return(e)

def load_monthly_scout(year,month,version):
    e=[]
    for day in range(1,monthrange(year,month)[1]+1):
        e.append(load_daily_scout(year,month,day,version))
    e=iris.cube.CubeList(e).merge_cube()
    e=e.collapsed('time', iris.analysis.MEAN)
    return e

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

def load_monthly_v3(year,month):
    e=[]
    dts=None
    m=None
    for member in range(1,81):
        h=iris.load_cube('%s/20CR/version_3/monthly_means/%04d/PRMSL.%04d.mnmean_mem%03d.nc' % 
                                                           (os.getenv('SCRATCH'),year,year,member),
                         iris.Constraint(name='Pressure reduced to MSL') &
                             iris.Constraint(time=lambda cell: \
                                             cell.point.year == year and \
                                             cell.point.month == month))
        h.attributes=None
        h.add_aux_coord(iris.coords.AuxCoord(member, long_name='member')) 
        if m is None:
            m=[h]
        else:
            m.append(h)
    m=iris.cube.CubeList(m).merge_cube()
    return(m)

def load_daily(year,month,day,version='3'):
    if version=='3':
        return load_daily_v3(year,month,day)
    else:
        return load_daily_scout(year,month,day,version)

def load_monthly(year,month,version='3'):
    if version=='3':
        return load_monthly_v3(year,month)
    else:
        return load_monthly_scout(year,month,version)

def get_sample(min_lon=-180,max_lon=360,min_lat=-90,max_lat=90,
               year=None,month=None,
               climatology=None,
               version=3,
               new_grid=None):

    # Load the model data
    m=load_monthly(year,month,version=version)

    # Anomalise
    if climatology is not None:
        midx=month-1
        m.data -= climatology[midx].data

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

