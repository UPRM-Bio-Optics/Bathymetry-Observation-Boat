import serial
import pynmea2

with serial.Serial('/dev/ttyS0', baudrate=4800, timeout=1) as ser:
    # read 10 lines from the serial output
    for i in range(10):
        line = ser.readline()#.decode('ascii', errors='replace')
        pynmea2.parse(line)
        print(line.strip())
        
