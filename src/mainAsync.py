import asyncio
import serial
import pynmea2
import csv
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
from dronekit import connect
from datetime import date
from time import sleep
import os
import dronekit_sitl
import pandas as pd

from bokeh.io import output_notebook
from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import HoverTool
from bokeh.io import export_png
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.models import ColorBar
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
    ############################################################################################################################################################################
def MapOverlay(csvpath: str, zoom=16, map_type='roadmap'):
    
    api_key = os.environ['GOOGLE_API_KEY']
    bokeh_width, bokeh_height = 500,400
    
    df = pd.read_csv(csvpath)

    lat = np.mean(df.Latitude)
    lon = np.mean(df.Longitude)
    
    gmap_options = GMapOptions(lat=lat, lng=lon,
                               map_type=map_type, zoom=zoom)
    hover = HoverTool(
        tooltips=[
            ('Depth in Feet', '@Depth_in_Feet '),
            # the {0.} means that we don't want decimals
            # for 1 decimal, write {0.0}
        ]
    )
    p = gmap(api_key, gmap_options, title='Bathymetry Map Parguera',
             width=bokeh_width, height=bokeh_height,
             tools=[hover, 'reset', 'wheel_zoom', 'pan'])
    source = ColumnDataSource(df)
    # defining a color mapper, that will map values of pricem2
    # between 2000 and 8000 on the color palette
    mapper = linear_cmap('Depth_in_Feet', palette, min(df.Depth_in_Feet), max(df.Depth_in_Feet))
    # we use the mapper for the color of the circles
    center = p.circle('Longitude', 'Latitude', radius='radius', alpha=0.4,
                      color=mapper, source=source)
    # and we add a color scale to see which values the colors
    # correspond to
    color_bar = ColorBar(color_mapper=mapper['transform'],
                         location=(0, 0))
    p.add_layout(color_bar, 'right')
    p.background_fill_color = None
    p.border_fill_color = None

    today = date.today().strftime("%b-%d-%Y")
    filename = os.getcwd() + '/Data/Graphs/'+ today + "MapOverlay.png"
    export_png(p, filename=filename)
    return p

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
                await asyncio.sleep(0.5)
                
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
def Contour(csvpath: str, threeD=False) -> None:
    
    
    df = pd.read_csv(csvpath)
    lat = df.Latitude
    lon = df.Longitude
    topo = df.Depth_in_Feet
    
    if(threeD):
        fig, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
        fileName = "ThreeD Map.png"
    else:
        fig, ax1 = plt.subplots()
        fileName = "TwoD Map.png"

    fig.set_figheight(10)
    fig.set_figwidth(15)
    xi = np.linspace(min(lon), max(lon), len(lon))
    yi = np.linspace(min(lat), max(lat), len(lat))

    zi = griddata((lon, lat), 
                  topo,
                  (xi[None, :], yi[:, None]), 
                  method='linear')

    cntr1 = ax1.contourf(xi, yi, zi, levels=30, cmap=cm.coolwarm)
    cbar = fig.colorbar(cntr1, ax=ax1)
    cbar.set_label('Depth in Feet', fontsize=20)

    # uncomment to see where each sample was taken
    #ax1.plot(lon, lat, 'bo', ms=1)

    ax1.set(xlim=(min(lon), max(lon)), ylim=(min(lat), max(lat)))

    ax1.set_title('Bathymetry Map in Parguera', fontsize=20)
    ax1.set_xlabel('Latitude', fontsize=20)
    ax1.set_ylabel('Longitude', fontsize=20)

    today = date.today().strftime("%b-%d-%Y")
    plt.savefig(os.getcwd() + '/Data/Graphs/'+ today + fileName)

    
    if(threeD):
        return
    Contour(csvpath, threeD=True)
    
 
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