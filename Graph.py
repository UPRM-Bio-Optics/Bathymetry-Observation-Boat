import os
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.interpolate


def getData() -> np.array(object):
    # import basemap module

    filename = os.getcwd() + '/data/topo.csv'

    lat, lon, topo = np.loadtxt(filename, delimiter=',', skiprows=2, unpack=True)

    resolution = 0.008333333333333333

    # Determine the number of grid points in the x and y directions
    nx = complex(0, (max(lon) - min(lon)) / resolution)
    ny = complex(0, (max(lat) - min(lat)) / resolution)

    # Build 2 grids: One with lats and the other with lons
    grid_x, grid_y = np.mgrid[min(lon):max(lon):nx, min(lat):max(lat):ny]

    # Interpolate topo into a grid (x by y dimesions)
    grid_z = scipy.interpolate.griddata((lon, lat), topo, (grid_x, grid_y), method='cubic')
    # Return Grids to plot Contourf
    return grid_x, grid_y, grid_z


def run2d() -> None:
    """
    :rtype: object
    """
    # get data to plot
    grid_x, grid_y, grid_z = getData()

    # plot
    cs = plt.contourf(grid_x, grid_y, grid_z, cmap=cm.coolwarm)
    plt.xlabel("Longitude", fontsize=15)
    plt.ylabel("Latitude", fontsize=15)
    plt.suptitle("Bathymetry Example", fontsize=18)
    plt.colorbar()
    # save Image and show it
    # plt.savefig(os.getcwd() + '/Graphs/TwoD map.png')
    plt.show()


def run3d() -> None:
    grid_x, grid_y, grid_z = getData()

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap=cm.coolwarm)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.suptitle('Topograhy Surface Render', fontsize=18)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    # plt.savefig(os.getcwd() + '/Graphs/ThreeD map.png')
    plt.show()
