import sys
import glob
from configparser import ParsingError
import serial
import pynmea2


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
    with serial.Serial('/dev/ttyS0', baudrate=4800, timeout=1) as ser:
        for i in range(15):

            line = ser.readline().decode('ascii', 'ignore')
            try:
                obj = pynmea2.parse(line)
            except ParsingError:
                print(f'Could Not Parse Data: {line} ')
                print(line.startswith('$'))
                continue

            if obj.sentence_type == 'DPT':
                print(f'Some depth data for you, NMEA GOD: DEPTH = {obj.depth} meters')
            elif obj.sentence_type == 'GGA':
                print(f'Some coordinates for you, NMEA GOD: LAT = {obj.latitude}, LON = {obj.longitude} ')
            else:
                print(f'Some other NMEA sentence of type: {obj.sentence_type} ')

        print('DONE!!!!')
