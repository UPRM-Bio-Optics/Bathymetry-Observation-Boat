import numpy
import serial
import pynmea2
import os
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
from matplotlib import cm
from dronekit import connect
from datetime import date
from time import sleep


def graph2d(lon, lat, topo):

    resolution = 0.008333333333333333
    # Determine the number of grid points in the x and y directions
    nx = complex(0, (max(lon) - min(lon)) / resolution)
    ny = complex(0, (max(lat) - min(lat)) / resolution)

    # Build 2 grids: One with lats and the other with lons
    grid_x, grid_y = np.mgrid[min(lon):max(lon):nx, min(lat):max(lat):ny]

    # Interpolate topo into a grid (x by y dimesions)
    grid_z = scipy.interpolate.griddata(
        (lon, lat), topo, (grid_x, grid_y), method='cubic')

    # plot
    cs = plt.contourf(grid_x, grid_y, grid_z, cmap=cm.coolwarm)
    plt.xlabel("Longitude", fontsize=15)
    plt.ylabel("Latitude", fontsize=15)
    plt.suptitle("Bathymetry Example", fontsize=18)
    plt.colorbar()
    # save Image and show it

    plt.savefig(os.getcwd() + '/src/Graphs/TwoD map.png')
    # plt.show()


def graph3d(lon, lat, topo):

    resolution = 0.008333333333333333
    # Determine the number of grid points in the x and y directions
    nx = complex(0, (max(lon) - min(lon)) / resolution)
    ny = complex(0, (max(lat) - min(lat)) / resolution)

    # Build 2 grids: One with lats and the other with lons
    grid_x, grid_y = np.mgrid[min(lon):max(lon):nx, min(lat):max(lat):ny]

    # Interpolate topo into a grid (x by y dimesions)
    grid_z = scipy.interpolate.griddata(
        (lon, lat), topo, (grid_x, grid_y), method='cubic')

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap=cm.coolwarm)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.suptitle('Topograhy Surface Render', fontsize=18)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.savefig(os.getcwd() + '/src/Graphs/ThreeD map.png')
    # plt.show()


def run():

    _vehicle_port = '/dev/USB0'  # dummy port; i forgor the port name
    _echoounder_port = '/dev/ttyS0'  # same here lol

    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    today = date.today()

    csvfile = open(os.getcwd() + f'/src/Data/depth_data - ' +
                today.strftime("%b-%d-%Y") + '.csv')
    writer = csv.writer(csvfile)
    _header = ['Latitude', 'Longitude', 'Depth in Meters']
    writer.writerow(_header)

    try:
        vehicle = connect(_vehicle_port, baudrate=115200, heartbeat_timeout=10)
        _scannable = vehicle.mode == 'AUTO' or vehicle.mode == 'LOITER' or vehicle.mode == 'MANUAL'

        with serial.Serial(_echoounder_port, baudrate=4800, timeout=2) as ser:
            while True:
                while _scannable:
                    line = ser.readline().decode('ascii', 'ignore')
                    nmea_object = pynmea2.parse(line)
                    row = [0, 0, 0]
                    
                    if nmea_object.sentence_type == 'DPT':
                        np.append(topo, nmea_object.depth)
                        row[2] = nmea_object.depth
                        
                    elif nmea_object.sentence_type == 'GGA':
                        np.append(lat, nmea_object.latitude)
                        np.append(lon, nmea_object.longitude)
                        
                        row[0] = nmea_object.latitude
                        row[1] = nmea_object.longitude
                    
                    if row[0] != 0 and row[1] != 0 and row [2] != 0:
                        writer.writerow(row)
                        time.sleep(1)
                    
                    
                are_empty = lat.size == 0 or lon.size == 0 or topo.size == 0
                if not _scannable and not are_empty:
                    break
            graph2d(lon, lat, topo)
            graph3d(lon, lat, topo)
    except:
        run()

if __name__ == '__main__':
    run()
