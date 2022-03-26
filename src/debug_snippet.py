from cProfile import label
from msilib.schema import Font
import sys
import glob
import serial
import pynmea2
import numpy as np
import time
import csv
import os
from datetime import date
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib import cm
from mpl_toolkits import basemap
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


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


def graphTest():

    file = open("Mar-25-2022.csv")
    csvReader = csv.reader(file)
    header = next(csvReader)
    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    
    for row in csvReader:
        lat = np.append(lat, round(float(row[0]), 5))
        lon = np.append(lon, round(float(row[1]), 5))
        topo = np.append(topo, round(float(row[2]), 5))

    fig, ax1 = plt.subplots()     
    
    fig.set_figheight(10)
    fig.set_figwidth(15)
    xi = np.linspace(min(lat), max(lat), len(lat))
    yi = np.linspace(min(lon), max(lon), len(lon))
    zi = griddata((lat ,lon), topo, (xi[None,:], yi[:,None]), method='linear')
    
    
    cntr1 = ax1.contourf(xi, yi, zi, levels=20, cmap= cm.coolwarm)
    cbar = fig.colorbar(cntr1, ax=ax1)
    cbar.set_label('Depth in Feet', fontsize = 20)
    ax1.plot(lat, lon, 'ro', ms=3)
    ax1.set(xlim=(min(lat), max(lat)), ylim=(min(lon), max(lon)))
    
    m = basemap.Basemap(llcrnrlat= min(lat), llcrnrlon= min(lon), 
                        urcrnrlat= max(lat), urcrnrlon=max(lon), 
                        width= max(lat) - min(lat), 
                        height= max(lon) - min(lon),
                        projection='merc',
                        resolution='c')
    
    ax1.set_title('Bathymetry Map in Parguera', fontsize = 20)
    ax1.set_xlabel('Latitude', fontsize = 20)
    ax1.set_ylabel('Longitude', fontsize = 20)
    plt.savefig("test.png", dpi= 300)
    plt.show()
    
    


if __name__ == '__main__':
    graphTest()