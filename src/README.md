# Echo Sounder Data Logger for Autonomous Surface Vehicle 

## Overview
This Python script interfaces with a Pixhawk autopilot and an echosounder to log depth and GPS data during a boat mission. The script connects to the Pixhawk using DroneKit, reads echosounder data via serial communication, and logs the information into a CSV file. Additionally, it provides real-time feedback on the battery status using the PiJuice library.

## Features
- Connects to Pixhawk autopilot for mission control.
- Logs depth and GPS data into a CSV file for later analysis.
- Monitors and displays PiJuice battery hat status.
- Utilizes DroneKit for Pixhawk communication and control.
- Handles exceptions and continues running to ensure continuous data logging.

## Requirements
- DroneKit: Install using `pip install dronekit`.
- PiJuice: Install using `pip install pijuice`.
- Pynmea2: Install using `pip install pynmea2`.

## Usage
1. Connect the Pixhawk autopilot to the designated port (`/dev/ttyACM0` ).
2. Connect the echosounder to the designated port (`/dev/ttyUSB0`).
3. Ensure that the required libraries are installed using the provided `pip install` commands.
4. Run the script using `python3 src/main.py`.
5. The script will continuously log data until the boat mission is completed or the script is manually stopped.

## Output
The script will create a CSV file in the `Data/echo_sounder/` directory, named with the current date (`%b-%d-%Y.csv`). The file will contain columns for latitude, longitude, and depth in feet.

## Notes
- Customize the script based on specific Pixhawk and echosounder configurations.
- Ensure that the Raspberry Pi or similar device running the script has the required permissions to access the serial ports.

## TO-DO
- Parallelize sensor data collection 
- refactoring of source code
