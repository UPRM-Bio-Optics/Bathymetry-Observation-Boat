import asyncio
from configparser import ParsingError
import serial
import pynmea2
import os
import csv
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
from matplotlib import cm
from dronekit import connect
from datetime import date
from time import sleep


class Drone:
    def __init__(self):
        # do whatever on startup, could be setting up files, directories, maybe the data structures to use.
        self._vehicle_port = '/dev/ttyACM0'  # dummy port; i forgor the port name
        self._echosounder_port = '/dev/ttyUSB0'  # same here lol
        self.dataDict = {'lat': np.array([]), 'lon': np.array([]), 'topo': np.array([])}
        today = date.today().strftime("%b-%d-%Y")
        # create txt file for error logs...
        are_empty = self.dataDict['lat'].size == 0 or self.dataDict['lon'].size == 0 or self.dataDict['topo'].size == 0

        self.csvfile = open(os.getcwd() + '/Data/depth_data/' + today + '.csv', 'w')
        self.writer = csv.writer(self.csvfile)
        _header = ['Latitude', 'Longitude', 'Depth in Meters']
        self.writer.writerow(_header)

        while True:
            try:
                self.vehicle = connect(self._vehicle_port, baud=115200, heartbeat_timeout=5)
                self.cmds = self.vehicle.commands
                self.cmds.download()
                self.cmds.wait_ready()
                self.missionlist = []
                break
            
            except Exception as e:
                print('Could not connect to Pixhawk')
                print (e)
                continue
        for cmd in self.cmds:
            self.missionlist.append(cmd)

    #############################################################################################################################################
    async def graph2d(self, lon, lat, topo):

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

    ############################################################################################################################################################################
    async def graph3d(self, lon, lat, topo):

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

    #####################################################################################################################################################################################
    async def run(self):
        _scannable = (self.vehicle.mode == 'AUTO' or self.vehicle.mode ==
                      'LOITER' or self.vehicle.mode == 'MANUAL') or self.cmds.next <= len(self.missionlist)
        print("About to enter loop.")
        with serial.Serial(self._echosounder_port, baudrate=4800, timeout=2) as ser:
            rows = 0
            for i in range(10): # for testing without pixhawk, uncomment above line to test with pixhawk.
            #while _scannable:
                try:
                    line = ser.readline().decode('ascii', 'ignore')
                    nmea_object = pynmea2.parse(line)
                    row = [None, None, 1]
                except Exception:
                    continue

                if nmea_object.sentence_type == 'DPT':
                    np.append(self.dataDict['topo'], nmea_object.depth)
                    row[2] = nmea_object.depth

                elif nmea_object.sentence_type == 'GGA':
                    print("Appending GPS data: ", nmea_object.latitude, nmea_object.longitude)
                    np.append(self.dataDict['lat'], nmea_object.latitude)
                    np.append(self.dataDict['lon'], nmea_object.longitude)

                    row[0] = nmea_object.latitude
                    row[1] = nmea_object.longitude

                if all(row):
                    print('Adding row to csv')
                    self.writer.writerow(row)
                    rows+=1
                _scannable = self.vehicle.armed
                print("Vehicle armed status: ", _scannable)
                await asyncio.sleep(2)
                
        print("Done with mission.")
         # try:
                
    #     graph2d(lon, lat, topo)
    #     graph3d(lon, lat, topo)
    # except Exception as e:
         
    #     print(' AT least you tried graphs :l')
    #     row = ['could not graph', 'error', e]
    #     writer.writerow(row)
        self.csvfile.close()
        # await self.graph2d(self.dataDict['lon'], self.dataDict['lat'], self.dataDict['topo'])
        # await self.graph3d(self.dataDict['lon'], self.dataDict['lat'], self.dataDict['topo'])
class dummyObject:
    async def printThing(self):
        while True:
            print("That other loop is sleeping :O")
            await asyncio.sleep(2)
        
    

async def main():
    loop = asyncio.get_event_loop()  # this handles loop
    drone = Drone()
    dummy = dummyObject()
    try:
        # await asyncio.ensure_future(drone.run())
        # await asyncio.ensure_future(dummy.printThing())# We ensure the future for all the tasks we want.
        # ^^^^^^^^^^^^^^ That ensure future does NOT work.
        await asyncio.gather(drone.run(), dummy.printThing()) #Gather works, just add the loops here and the couroutines will work when the others are sleeping.
        #loop.run_forever()  # Loop runs forever
    except KeyboardInterrupt:  # We can interrupt the program with CTRL^C etc
        pass


if __name__ == '__main__':
    asyncio.run(main())

  
