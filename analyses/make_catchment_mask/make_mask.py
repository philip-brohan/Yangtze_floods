#!/usr/bin/env python

# Make a mask on the 20CRv3 PRMSL grid showing which points are in the 
#  Yangtze catchment.

import os
import iris
import numpy
import geopandas
from shapely.geometry import Point

# Read the shapefile and extract the polygon for the Yangtze
rivers=geopandas.read_file('Major_Basins_of_the_World.shp')
yangtze=rivers[rivers['NAME'] == 'Yangtze']

# Get a 20CRv3 field to use as the grid
rGrid = iris.load_cube("%s/20CR/version_3/normals/PRMSL/climatology_1981_2010/010100.nc" % os.getenv("DATADIR"))

# Convert the field to an in=1, out=0 mask
lats=rGrid.coord('latitude').points
lons=rGrid.coord('longitude').points
[lon2d,lat2d]=numpy.meshgrid(lons,lats)
lon2 = lon2d.reshape(-1) # to 1d for iteration
lat2 = lat2d.reshape(-1)
mask = []
for lat, lon in zip(lat2, lon2):
    this_point = geopandas.GeoSeries([Point(lon, lat)],crs=yangtze.crs,index=yangtze.index)
    res = yangtze.geometry.contains(this_point)
    mask.append(res.values[0])

mask = numpy.array(mask).reshape(lon2d.shape)
mask = mask*1
rGrid.data = mask
iris.save(rGrid,'mask.nc')
