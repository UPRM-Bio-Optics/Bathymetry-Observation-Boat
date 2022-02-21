import asyncio
from configparser import ParsingError
import numpy
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
        self._vehicle_port = '/dev/USB0'  # dummy port; i forgor the port name
        self._echoounder_port = '/dev/ttyS0'  # same here lol

        lat = np.array([])
        lon = np.array([])
        topo = np.array([])
        today = date.today()
        # create txt file for error logs...
        are_empty = lat.size == 0 or lon.size == 0 or topo.size == 0

        self.csvfile = open(os.getcwd() + f'/src/Data/depth_data - ' +
                       today.strftime("%b-%d-%Y") + '.csv')
        writer = csv.writer(self.csvfile)
        _header = ['Latitude', 'Longitude', 'Depth in Meters']
        writer.writerow(_header)

        self.vehicle = connect(self._vehicle_port, baud=115200, heartbeat_timeout=5)
        cmds = self.vehicle.commands
        cmds.download()
        cmds.wait_ready()
        missionlist = []
        for cmd in cmds:
            missionlist.append(cmd)


#####################################################################################################################################################################################
    async def run(self):
        _scannable = (self.vehicle.mode == 'AUTO' or self.vehicle.mode ==
                      'LOITER' or self.vehicle.mode == 'MANUAL') and self.cmds.next <= len(self.missionlist)

        with serial.Serial(self._echoounder_port, baudrate=4800, timeout=2) as ser:
            while _scannable:
                try:
                    line = ser.readline().decode('ascii', 'ignore')
                    nmea_object = pynmea2.parse(line)
                    row = [None, None, None]
                except ParsingError:
                    continue

                if nmea_object.sentence_type == 'DPT':
                    np.append(self.topo, nmea_object.depth)
                    row[2] = nmea_object.depth

                elif nmea_object.sentence_type == 'GGA':
                    np.append(self.lat, nmea_object.latitude)
                    np.append(self.lon, nmea_object.longitude)

                    row[0] = nmea_object.latitude
                    row[1] = nmea_object.longitude

                if all(row):
                    self.writer.writerow(row)
                    sleep(1)

        self.csvfile.close()
        graph2d(lon, lat, topo)
        graph3d(lon, lat, topo)


async def main():
