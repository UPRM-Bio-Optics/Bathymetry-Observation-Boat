import sys
import glob
import serial
import pynmea2
import numpy as np
import time
import csv
import os
from datetime import date

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

if __name__ == '__main__':
    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    today = date.today()
    csvfilePath = 'Data/depth_data/' + today.strftime("%b-%d-%Y") + '.csv'
    csvfile = open(csvfilePath, 'w')
        
    #csvfile = open(os.getcwd() + f'/src/Data/depth_data/' +
                   #today.strftime("%b-%d-%Y") + '.csv')
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
                print('Could Not Parse Data: ', line) # print(f'was not working.)
                print(line.startswith('$'))
                continue

            if obj.sentence_type == 'DPT':
                print('Some depth data for you, NMEA GOD: DEPTH = ', obj.depth) #print(f'Some depth data for you, NMEA GOD: DEPTH = {obj.depth} meters')
                row[2] = 1
            elif obj.sentence_type == 'GGA':
                print('Some coordinates for you, NMEA GOD: LAT = ', obj.latitude)
                np.append(lat, obj.latitude)
                print('Some coordinates for you, NMEA GOD: LON = ', obj.longitude) #print(f'Some coordinates for you, NMEA GOD: LAT = {obj.latitude}, LON = {obj.longitude} ')
                np.append(lon, obj.lon)
                row[0] = obj.latitude
                row[1] = obj.longitude
            if all(row):
                writer.writerow(row)
                #time.sleep(1)
            else:
                print('Some other NMEA sentence of type: ', obj.sentence_type)
            
            #time.sleep(5)
        temp = [1,2,3] #temp data
        writer.writerow(temp)
        csvfile.close()
        print('DONE!!!!')
