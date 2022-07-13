#!/usr/bin/python3
import serial
import pynmea2
import csv
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
from dronekit import connect
from datetime import date
from time import sleep, time
import os
#import dronekit_sitl
import pandas as pd

from bokeh.plotting import gmap, figure
from bokeh.models import GMapOptions, HoverTool, LogTicker, ColorBar, ColumnDataSource
from bokeh.io import export_png
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.layouts import row

#lib only available in rpi
from pijuice import PiJuice
'''
TODO
- make scannable variable into function -> boolean
'''

def Contour(csvpath: str, threeD=False) -> None:
    """ 
    creates contour plot from topographical data obtained from echosounder


    Args:
        csvpath (str): path to csv containing data: Lat, Lon, Depth in feet
        threeD (bool, optional): boolean flag to determine which map to make; 2D or 3D. 
            Defaults to False.
    """

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
    plt.savefig(os.sep.join([os.getcwd(),"Data","Graphs",today + fileName]))

    if(threeD):
        return
    Contour(csvpath, threeD=True)


def MapOverlay(csvpath: str, zoom=18, map_type='satellite') -> row:
    """ Creates overlay of Depth Data with a map. 

    Args:
        csvpath (str): Path to csv containing data: Lat, Lon, Depth in feet
        zoom (int, optional):  Defaults to 18.
        map_type (str, optional): type of google map. Defaults to 'satellite'.

    Returns:
        row: bokeh row object
    """
    api_key = os.environ['GOOGLE_API_KEY']
    bokeh_width, bokeh_height = 500, 400

    df = pd.read_csv(csvpath)
    # wack ass line to test different radius
    df['radius'] = np.sqrt(df['Depth_in_Feet']) / (zoom - (zoom - 20))

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
    mapper = linear_cmap('Depth_in_Feet', palette, min(
        df.Depth_in_Feet), max(df.Depth_in_Feet))
    # we use the mapper for the color of the circles
    center = p.circle('Longitude', 'Latitude', radius='radius', alpha=0.4,
                      color=mapper, source=source)
    # and we add a color scale to see which values the colors
    # correspond to
    color_bar = ColorBar(color_mapper=mapper['transform'],
                         location=(0, 0), label_standoff=12,
                         ticker=LogTicker(), border_line_color=None
                         )

    color_bar_title = figure(title='Depth in Feet', title_location='left',
                             height=400,
                             width=200,
                             toolbar_location=None, min_border=0,
                             outline_line_color=None
                             )

    color_bar_title.add_layout(color_bar, 'left')
    color_bar_title.title.align = "center"
    color_bar_title.title.text_font_size = '12pt'

    pu = row(p, color_bar_title)
    today = date.today().strftime("%b-%d-%Y")
    filename = os.sep.join([os.getcwd(),"Data","Graphs",today + "MapOverlay.png"])
    export_png(pu, filename=filename)
    return pu


def batteryStatus() -> None:
    """ Prints Output of PiJuice Battery Hat Status 

    Args: None
    """
    pijuice = PiJuice()
    battery_level = pijuice.status.GetChargeLevel()['data']
    battery_status = pijuice.status.GetStatus()['data']
    battery_tempeture = pijuice.status.GetBatteryTemperature()['data']
    print(f'\nPiJuice Battery Percentage is: {battery_level}%\n')
    print(f'The PiJuice Battery Status is: {battery_status}\n')
    print(
        f'The Pijuice Hat Temperture is: {battery_tempeture}°C  \nTempeture in debugging: 24°C\n')


def isScannable(vehicle, cmds, missionlist) -> bool:
    """
    Args:
        vehicle (DroneKit object): 
        cmds (iterable): vehicle command / waypoints 
        missionlist (iterable): list created from cmds

    Returns:
        bool: is Mission Finished.
    """
    return vehicle.armed or cmds.next <= len(missionlist)


def main() -> None:
    """
    Main Program to be executed
    """
    # Initialize ports for pixhawk and echosounder
    _vehicle_port = '/dev/ttyACM0'
    _echosounder_port = '/dev/ttyUSB0'

    # Initialize data lists
    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    today = date.today().strftime("%b-%d-%Y")

    # Create and initialize csv file
    csvfile = open(os.getcwd() + '/Data/depth_data/' + today + '.csv', 'w')
    writer = csv.writer(csvfile)
    _header = ['Latitude', 'Longitude', 'Depth_in_Feet']
    writer.writerow(_header)

    # Pixhawk connection loop
    while True:
        try:
            vehicle = connect(_vehicle_port, baud=115200, heartbeat_timeout=5)
            # Download comands
            cmds = vehicle.commands
            cmds.download()
            cmds.wait_ready()
            # Initialize list of missions
            missionlist = []
            break

        except Exception as e:
            print('Could not connect to Pixhawk')
            print(e)
            continue

    # Add all commands to the list of missions
    for cmd in cmds:
        missionlist.append(cmd)

    # Sensor connection
    print("about to enter loop")
    ser = serial.Serial(_echosounder_port, baudrate=4800, timeout=2)
    row = [None, None, None]
    scannable = vehicle.armed
    currentWaypoint = vehicle.commands.next
    # for i in range(50): #stop deleting this

    clock = time()
    #run loop for as long as the boat is in the water
    while scannable:

        # Translate NMEA data to sentences
        try:
            line = ser.readline().decode('ascii', 'ignore')
            nmea_object = pynmea2.parse(line)

        except Exception:
            continue

        # Detect and record depth data sentences
        if nmea_object.sentence_type == 'DBT' and nmea_object.depth_feet is not None:

            print(f'Appending Depth Data {nmea_object.depth_feet}')
            topo = np.append(topo, float(nmea_object.depth_feet))
            row[2] = nmea_object.depth_feet

        # Detect and record location data sentences
        elif nmea_object.sentence_type == 'GGA':

            print(
                f'Appending GPS Data:  Lat = {nmea_object.latitude} Lon = {nmea_object.longitude}')
            lat = np.append(lat, nmea_object.latitude)
            lon = np.append(lon, nmea_object.longitude)
            row[0] = nmea_object.latitude
            row[1] = nmea_object.longitude

        # Write data to CSV file
        if all(row):
            print('ADDING ROW CSV')
            writer.writerow(row)
            csvfile.flush()    # Save current data to CSV
            row = [None, None, None]
            sleep(0.1)
        # update scannable variable
        scannable = vehicle.armed  # and currentWaypoint <= len(missionlist)
        #currentWaypoint = vehicle.commands.next

        # print battery status every minute then reset counter
        if clock - time() > 60:
            batteryStatus()
            clock = time()

    print('Done with Mission ')

    # Graph CSV data
    try:
        Contour(csvfile.name)
        MapOverlay(csvfile.name)

    except Exception as e:

        print(' AT least you tried graphs :|')
        row = ['could not graph', 'error', e]
        writer.writerow(row)

    # Close CSV file and EchoSounder Port
    csvfile.close()
    ser.close()


if __name__ == '__main__':
    main()
