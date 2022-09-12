import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import os
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    if GPIO.input(15) == GPIO.LOW:
        print("Button was pushed!")
        os.system("python3 /home/pi/NCAS-M/NCAS-UPRM/Remote/client.py")
        