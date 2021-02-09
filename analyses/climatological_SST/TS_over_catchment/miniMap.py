# Function to add a mini-map to a time-series plot
import os
import datetime
import numpy

import iris
import iris.time

import IRData.twcr as twcr
import warnings

import cmocean

import matplotlib
from matplotlib.patches import Rectangle

# Load the mask fields
landMask = iris.load_cube(
    "%s/fixed_fields/land_mask/opfc_global_2019.nc" % os.getenv("DATADIR")
)
catchmentMask = iris.load_cube(
    "%s/../../make_catchment_mask/mask.plot.nc" % os.path.dirname(__file__)
)

# Load the 20CR data
def getFiles(var, dte, offset, version, member):
    start = dte - datetime.timedelta(hours=offset)
    end = dte + datetime.timedelta(hours=offset)
    files = set()
    for year in range(start.year, end.year + 1):
        for month in range(1, 13):
            if year == start.year and month < start.month:
                continue
            if year == end.year and month > end.month:
                continue
            files.add(
                twcr.version_3_release.utils._get_data_file_name(
                    var, year, month, version=version, member=member
                )
            )
    return files


def loadSmoothed(var, dte, offset, version):
    coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    start = dte - datetime.timedelta(hours=offset)
    pStart = iris.time.PartialDateTime(
        year=start.year, month=start.month, day=start.day, hour=start.hour
    )
    end = dte + datetime.timedelta(hours=offset)
    pEnd = iris.time.PartialDateTime(
        year=end.year, month=end.month, day=end.day, hour=end.hour
    )
    timeConstraint = lambda c: pStart <= c < pEnd
    result = iris.cube.CubeList()
    for member in range(1, 81):
        accum = iris.cube.CubeList()
        for file_name in getFiles(var, dte, offset, version, member):
            try:
                with warnings.catch_warnings():  # Iris is v.fussy
                    warnings.simplefilter("ignore")
                    hslice = iris.load_cube(
                        file_name, iris.Constraint(time=timeConstraint)
                    )
                    # fix the geometry metadata
                    hslice.coord("latitude").coord_system = coord_s
                    hslice.coord("longitude").coord_system = coord_s
            except iris.exceptions.ConstraintMismatchError:
                raise Exception(
                    "%s not available for %04d-%02d-%02d:%02d"
                    % (var, dte.year, dte.month, dte.day, dte.hour)
                )
            accum.append(hslice.copy())
        devN = iris.util.equalise_attributes(accum)
        accum = accum.concatenate_cube()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            accum = accum.collapsed("time", iris.analysis.MEAN)
        accum.add_aux_coord(iris.coords.AuxCoord(member, long_name="member"))
        result.append(accum)
    devN = iris.util.equalise_attributes(result)
    result = result.merge_cube()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = result.collapsed("member", iris.analysis.MEAN)
    # Get rid of pointless extra dimensions (generally height)
    result = iris.util.squeeze(result)
    return result


# Create a dummy cube - centered on China with the size from the arguments.
#  Regrid everything onto this cube before plotting.
def makePlotCube(cs, resolution, xmin, xmax, ymin, ymax):

    lat_values = numpy.arange(ymin, ymax + resolution, resolution)
    latitude = iris.coords.DimCoord(
        lat_values, standard_name="latitude", units="degrees_north", coord_system=cs
    )
    lon_values = numpy.arange(xmin, xmax + resolution, resolution)
    longitude = iris.coords.DimCoord(
        lon_values, standard_name="longitude", units="degrees_east", coord_system=cs
    )
    dummy_data = numpy.zeros((len(lat_values), len(lon_values)))
    plot_cube = iris.cube.Cube(
        dummy_data, dim_coords_and_dims=[(latitude, 0), (longitude, 1)]
    )
    return plot_cube




def miniMap(
    ax,
    year,
    month,
    day,
    hour,
    var,
    version="3",
    xscale=96,
    yscale=54,
    zorder=100,
):

    dte = datetime.datetime(
        year, month, day, int(hour), int(hour % 1 * 60)
    )
    varF = loadSmoothed(var, dte, 36, version)

    # Lat and lon range (in rotated-pole coordinates) for plot
    ax.set_xlim(-1 * xscale / 2, xscale / 2)
    ax.set_ylim(-1 * yscale / 2, yscale / 2)
    ax.set_aspect("auto")

    plotCube = makePlotCube(
        iris.coord_systems.RotatedGeogCS(55.5, 287.5, 0),
        0.05,
        xscale * -0.5,
        xscale * 0.5,
        yscale * -0.5,
        yscale * 0.5,
    )

    # Background
    ax.add_patch(
        Rectangle(
            (-1 * xscale / 2, -1 * yscale / 2),
            xscale,
            yscale,
            facecolor=(0.6, 0.6, 0.6, 1),
            fill=True,
            zorder=zorder + 1,
        )
    )

    # Plot the land mask
    pField = landMask.regrid(plotCube, iris.analysis.Linear())
    lats = pField.coord("latitude").points
    lons = pField.coord("longitude").points
    pImg = ax.pcolorfast(
        lons,
        lats,
        pField.data,
        cmap=matplotlib.colors.ListedColormap(((0.4, 0.4, 0.4, 0), (0.4, 0.4, 0.4, 1))),
        vmin=0,
        vmax=1,
        alpha=1.0,
        zorder=zorder + 20,
    )

    # Plot the weather variable
    pField = varF.regrid(plotCube, iris.analysis.Linear())
    lats = pField.coord("latitude").points
    lons = pField.coord("longitude").points
    # Details are different for each variable
    if var == "PRMSL":
        pImg = ax.contourf(
            lons,
            lats,
            pField.data,
            31,
            cmap=cmocean.cm.diff,
            vmin=100000,
            vmax=103150,
            alpha=0.7,
            antialiased=True,
            zorder=zorder + 50,
        )
    if var == "TMP2m":
        pImg = ax.contourf(
            lons,
            lats,
            pField.data,
            31,
            cmap=cmocean.cm.balance,
            vmin=240,
            vmax=310,
            alpha=0.5,
            antialiased=True,
            zorder=zorder + 50,
        )
    if var == "PRATE":
        pImg = ax.contourf(
            lons,
            lats,
            pField.data,
            31,
            cmap=cmocean.cm.rain,
            vmin=0.0,
            vmax=0.0005,
            alpha=1.0,
            antialiased=True,
            zorder=zorder + 50,
        )
    if var == "PWAT":
        pImg = ax.contourf(
            lons,
            lats,
            pField.data,
            31,
            cmap=cmocean.cm.speed,
            vmin=0.0,
            vmax=70.0,
            alpha=0.5,
            antialiased=True,
            zorder=zorder + 50,
        )
    if var == "WEASD":
        #    print(numpy.max(pField.data))
        #    print(numpy.min(pField.data))
        pImg = ax.contourf(
            lons,
            lats,
            pField.data,
            31,
            cmap=cmocean.cm.ice_r,
            vmin=0.0,
            vmax=100.0,
            alpha=0.5,
            antialiased=True,
            zorder=zorder + 50,
        )
