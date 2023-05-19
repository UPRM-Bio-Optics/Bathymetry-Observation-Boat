#!/usr/bin/python3
# WARNING:bokeh.io.export:file:///home/pi/NCAS-M/NCAS-UPRM/bokeh8g8he3kx.html 538:2167 "[bokeh]" "could not set initial ranges"
import serial
import pynmea2
import csv
import numpy as np
import os


from dronekit import connect
from datetime import date
from time import sleep, time
from utils.graphs import MapOverlay, plotlyGraph


# lib only available in rpi
from pijuice import PiJuice

"""
TODO
- make scannable variable into function -> boolean
"""


def batteryStatus() -> None:
    """Prints Output of PiJuice Battery Hat Status

    Args: None
    """
    pijuice = PiJuice()
    battery_level = pijuice.status.GetChargeLevel()["data"]
    battery_status = pijuice.status.GetStatus()["data"]
    battery_tempeture = pijuice.status.GetBatteryTemperature()["data"]
    print(f"\nPiJuice Battery Percentage is: {battery_level}%\n")
    print(f"The PiJuice Battery Status is: {battery_status}\n")
    print(
        f"The Pijuice Hat Temperture is: {battery_tempeture}°C  \nTempeture in debugging: 24°C\n"
    )


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
    _vehicle_port = "/dev/ttyACM0"
    _echosounder_port = "/dev/ttyUSB0"

    # Initialize data lists
    lat = np.array([])
    lon = np.array([])
    topo = np.array([])
    today = date.today().strftime("%b-%d-%Y")

    # Create and initialize csv file
    csvfile = open(os.getcwd() + "/Data/echo_sounder/" + today + ".csv", "w")
    writer = csv.writer(csvfile)
    _header = ["Latitude", "Longitude", "Depth_in_Feet"]
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
            print("Could not connect to Pixhawk")
            print(e)
            continue

    # os.system("python3 ../Remote/listenerDronekit.py")
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
    # run loop for as long as the boat is in the water
    while True:
        print("Waiting for vehicle to be armed...")
        scannable = vehicle.armed
        sleep(1)
        if not scannable:
            continue
        while scannable:
            print("Vehicle is armed!")
            # Translate NMEA data to sentences
            try:
                line = ser.readline().decode("ascii", "ignore")
                nmea_object = pynmea2.parse(line)

            except Exception:
                continue

            # Detect and record depth data sentences
            if nmea_object.sentence_type == "DBT" and nmea_object.depth_feet is not None:
                print(f"Appending Depth Data {nmea_object.depth_feet}")
                topo = np.append(topo, float(nmea_object.depth_feet))
                row[2] = nmea_object.depth_feet

            # Detect and record location data sentences
            elif nmea_object.sentence_type == "GGA":
                print(
                    f"Appending GPS Data:  Lat = {nmea_object.latitude} Lon = {nmea_object.longitude}"
                )
                lat = np.append(lat, nmea_object.latitude)
                lon = np.append(lon, nmea_object.longitude)
                row[0] = nmea_object.latitude
                row[1] = nmea_object.longitude

            # Write data to CSV file
            if all(row):
                print("ADDING ROW CSV")
                writer.writerow(row)
                csvfile.flush()  # Save current data to CSV
                row = [None, None, None]
                sleep(0.1)
            # update scannable variable
            scannable = vehicle.armed  # and currentWaypoint <= len(missionlist)
            # currentWaypoint = vehicle.commands.next

            # print battery status every minute then reset counter
            if time() - clock > 30:
                batteryStatus()
                clock = time()
            
        break

            

    print("Done with Mission ")

    # Graph CSV data
    try:
        plotlyGraph(csvfile.name)
        MapOverlay(csvfile.name)

    except Exception as e:
        print(" AT least you tried graphs :|")
        row = ["could not graph", "error", e]
        writer.writerow(row)

    # Close CSV file and EchoSounder Port
    csvfile.close()
    ser.close()


if __name__ == "__main__":
    main()
