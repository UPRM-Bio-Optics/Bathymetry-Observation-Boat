
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
#import dronekit_sitl
import pandas as pd

from bokeh.plotting import gmap, figure
from bokeh.models import GMapOptions, HoverTool, LogTicker, ColorBar, ColumnDataSource
from bokeh.io import export_png
from bokeh.transform import linear_cmap
from bokeh.palettes import Plasma256 as palette
from bokeh.layouts import row


def main():
    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    today = date.today()
    csvfilePath = 'Data/depth_data/' + today.strftime("%b-%d-%Y") + '.csv'
    csvfile = open(csvfilePath, 'w')

    # csvfile = open(os.getcwd() + f'/src/Data/depth_data/' +
    # today.strftime("%b-%d-%Y") + '.csv')
    writer = csv.writer(csvfile)
    _header = ['Latitude', 'Longitude', 'Depth in Meters']
    writer.writerow(_header)
    with serial.Serial('/dev/ttyUSB0', baudrate=4800, timeout=1) as ser:
        for i in range(15):

            line = ser.readline().decode('ascii', 'ignore')
            row = [None, None, 1]
            try:
                obj = pynmea2.parse(line)
            except:
                # print(f'was not working.)
                print('Could Not Parse Data: ', line)
                print(line.startswith('$'))
                continue

            if obj.sentence_type == 'DPT':
                # print(f'Some depth data for you, NMEA GOD: DEPTH = {obj.depth} meters')
                print('Some depth data for you, NMEA GOD: DEPTH = ', obj.depth)
                row[2] = 1
            elif obj.sentence_type == 'GGA':
                print('Some coordinates for you, NMEA GOD: LAT = ', obj.latitude)
                np.append(lat, obj.latitude)
                # print(f'Some coordinates for you, NMEA GOD: LAT = {obj.latitude}, LON = {obj.longitude} ')
                print('Some coordinates for you, NMEA GOD: LON = ', obj.longitude)
                np.append(lon, obj.lon)
                row[0] = obj.latitude
                row[1] = obj.longitude
            if all(row):
                writer.writerow(row)
                # time.sleep(1)
            else:
                print('Some other NMEA sentence of type: ', obj.sentence_type)

            # time.sleep(5)
        temp = [1, 2, 3]  # temp data
        writer.writerow(temp)
        csvfile.close()
        print('DONE!!!!')


def graph(csvpath: str, threeD=False) -> None:
    
    
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

    ax1.set_title('Bathymetry Map in Parguera', fontsize=2, )
    ax1.set_xlabel('Latitude', fontsize=20)
    ax1.set_ylabel('Longitude', fontsize=20)

    today = date.today().strftime("%b-%d-%Y")
    plt.savefig(os.getcwd() + '/Data/Graphs/'+ today +' '+ fileName)

    
    if(threeD):
        return
    graph(csvpath, threeD=True)
    
    
def mapOverlay(csvpath: str, zoom=18, map_type='satellite'):
    
    api_key = os.environ['GOOGLE_API_KEY']
    bokeh_width, bokeh_height = 500,400
    
    df = pd.read_csv(csvpath)
    df['radius'] = np.sqrt(df['Depth_in_Feet'])/0.8
        
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
    color_bar_title.title.align="center"
    color_bar_title.title.text_font_size = '12pt'
 
    


    pu = row(p, color_bar_title)
    today = date.today().strftime("%b-%d-%Y")
    filename = os.getcwd() + '/Data/Graphs/'+ today + ' ' +"MapOverlay.png"
    export_png(pu, filename=filename)
    return pu
# Function to determines if vehicle is armed or not done with missions
if __name__ == '__main__':
    csvpath = os.getcwd() + '/Data/depth_data/Mar-25-2022.csv'
    graph(csvpath)
    mapOverlay(csvpath)