import os
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
def button_callback(channel):
    print("Button was pushed!")
    os.system("python3 /home/pi/NCAS-M/NCAS-UPRM/Remote/client.py")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(15,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
