
import serial
import pynmea2
import csv
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
from matplotlib import cm
from dronekit import connect
from datetime import date
from time import sleep
import os
import random
'''
TODO
- make scannable variable into function -> boolean
'''
# https://hacks.mozilla.org/2017/02/headless-raspberry-pi-configuration-over-bluetooth/


def graph2d(lon, lat, topo) -> None:

    resolution = 0.008333333333333333
    # Determine the number of grid points in the x and y directions
    nx = complex(0, (max(lon) - min(lon)) / resolution)
    ny = complex(0, (max(lat) - min(lat)) / resolution)

    # Build 2 grids: One with lats and the other with lons
    grid_x, grid_y = np.mgrid[min(lon):max(lon):nx, min(lat):max(lat):ny]

    # Interpolate topo into a grid (x by y dimesions)
    grid_z = scipy.interpolate.griddata(
        (lon, lat), topo, (grid_x, grid_y), method='linear')

    # plot
    plt.contourf(grid_x, grid_y, grid_z, cmap=cm.coolwarm)
    plt.xlabel("Longitude", fontsize=15)
    plt.ylabel("Latitude", fontsize=15)
    plt.suptitle("Bathymetry Example", fontsize=18)
    plt.colorbar()
    
    # save Image and show it
    today = date.today().strftime("%b-%d-%Y")
    plt.savefig(os.getcwd() + '/Data/Graphs/' + today + 'TwoD map.png')
    # plt.show()


def graph3d(lon, lat, topo) -> None:

    resolution = 0.008333333333333333
    # Determine the number of grid points in the x and y directions
    nx = complex(0, (max(lon) - min(lon)) / resolution)
    ny = complex(0, (max(lat) - min(lat)) / resolution)

    # Build 2 grids: One with lats and the other with lons
    grid_x, grid_y = np.mgrid[min(lon):max(lon):nx, min(lat):max(lat):ny]

    # Interpolate topo into a grid (x by y dimesions)
    grid_z = scipy.interpolate.griddata(
        (lon, lat), topo, (grid_x, grid_y), method='linear')

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap=cm.coolwarm)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.suptitle('Topograhy Surface Render', fontsize=18)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    today = date.today().strftime("%b-%d-%Y")
    plt.savefig(os.getcwd() + '/Data/Graphs/' + today + 'ThreeD map.png')
    # plt.show()


def isScannable(vehicle, cmds, missionlist) -> bool:
    return vehicle.armed or cmds.next <= len(missionlist)


def run():
    #ports for pixhawk and port for echosounder
    _vehicle_port = '/dev/ttyACM0'
    _echosounder_port = '/dev/ttyUSB0'

    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    today = date.today().strftime("%b-%d-%Y")

    csvfile = open(os.getcwd() + '/Data/depth_data/' + today + '.csv', 'w')
    writer = csv.writer(csvfile)
    _header = ['Latitude', 'Longitude', 'Depth in Feet']
    writer.writerow(_header)

    while True:
        try:
            vehicle = connect(_vehicle_port, baud=115200, heartbeat_timeout=5)
            cmds = vehicle.commands
            cmds.download()
            cmds.wait_ready()
            missionlist = []
            break

        except Exception as e:
            print('Could not connect to Pixhawk')
            print(e)
            continue

    for cmd in cmds:
        missionlist.append(cmd)

    print("about to enter loop")
    ser = serial.Serial(_echosounder_port, baudrate=4800, timeout=2)
    row = [None, None, None]
    scannable = vehicle.armed
    #for i in range(50): #stop deleting this
    while scannable:
          
        try:
            line = ser.readline().decode('ascii', 'ignore')
            nmea_object = pynmea2.parse(line)

        except Exception:
            continue

        if nmea_object.sentence_type == 'DBT':
            
                print(f'Appending Depth Data {nmea_object.depth_feet}')
                topo = np.append(topo, float(nmea_object.depth_feet))
                row[2] = nmea_object.depth_feet
                
                

        elif nmea_object.sentence_type == 'GGA':
            
            print(f'Appending GPS Data:  {nmea_object.latitude} {nmea_object.longitude}')
            lat = np.append(lat, nmea_object.latitude)
            lon = np.append(lon, nmea_object.longitude)
            row[0] = nmea_object.latitude
            row[1] = nmea_object.longitude
            
        print(row)

        if all(row):
            
            print('ADDING ROW CSV')
            writer.writerow(row)
            csvfile.flush()
            row = [None, None, None]
            sleep(0.1)
        scannable = vehicle.armed

    print('Done with Mission ')

    try:

        graph2d(lon, lat, topo)
        graph3d(lon, lat, topo)
    except Exception as e:

        print(' AT least you tried graphs :|')
        row = ['could not graph', 'error', e]
        writer.writerow(row)

    csvfile.close()
    ser.close()

if __name__ == '__main__':
    run()
