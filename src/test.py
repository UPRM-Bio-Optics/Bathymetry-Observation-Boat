import numpy
import serial
import pynmea2
import os
import numpy as np 
import scipy.interpolate
import matplotlib.pyplot as plt
from matplotlib import cm
from dronekit import connect 


def main():
    
    _vehicle_port = '/dev/USB0' # dummy port; i forgor the port name 
    _echoounder_port = '/dev/ttyS0' # same here lol

    lat = np.array([])
    lon = np.array([])
    topo = np.array([])

    try: 
        vehicle = connect(_vehicle_port, baudrate = 115200, heartbeat_timeout = 10)
        _scannable = vehicle.mode == 'AUTO' or vehicle.mode == 'LOITER'
        
        with serial.Serial(_echoounder_port, baudrate = 4800, timeout = 2) as ser:
            
            while True:
                
                while _scannable:
                    line = ser.readline().decode('ascii', 'ignore')
                    nmea_object = pynmea2.parse(line)
                    if nmea_object.sentence_type == 'DPT':
                        np.append(topo, nmea_object.depth)
                        
                    elif nmea_object.sentence_type == 'GGA':
                        np.append(lat, nmea_object.latitude)
                        np.append(lon, nmea_object.longitude)
                
                are_empty = lat.size == 0 or lon.size == 0 or topo.numpy.size == 0
                if not vehicle.armed and not are_empty:
                    break
            
            
            resolution = 0.008333333333333333
            # Determine the number of grid points in the x and y directions
            nx = complex(0, (max(lon) - min(lon)) / resolution)
            ny = complex(0, (max(lat) - min(lat)) / resolution)
            
            # Build 2 grids: One with lats and the other with lons
            grid_x, grid_y = np.mgrid[min(lon):max(lon):nx, min(lat):max(lat):ny]
            
            # Interpolate topo into a grid (x by y dimesions)
            grid_z = scipy.interpolate.griddata((lon, lat), topo, (grid_x, grid_y), method='cubic')
            
            # plot
            cs = plt.contourf(grid_x, grid_y, grid_z, cmap=cm.coolwarm)
            plt.xlabel("Longitude", fontsize=15)
            plt.ylabel("Latitude", fontsize=15)
            plt.suptitle("Bathymetry Example", fontsize=18)
            plt.colorbar()
            # save Image and show it
            plt.savefig(os.getcwd() + '/Graphs/TwoD map.png') #TODO apply aproppiate working directory  
            plt.show()
    except:
        print('Sum Happened, maybe you oughtta format this better ')

if __name__ == '__main__':
    main()