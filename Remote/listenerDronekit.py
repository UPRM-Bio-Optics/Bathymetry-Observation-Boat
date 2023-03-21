import paho.mqtt.client as mqtt
import os
from time import sleep
from dronekit import connect, LocationGlobal, VehicleMode

'''
This is the Subscriber and it is used to listen for the ngrok IP published by the RPI on the broker.
Once it receives the IP it attempts to connect via ssh
'''


def returnHome():
    home = vehicle.home_location
    vehicle.simple_goto(home)


def setMode(mode):
    vehicle.mode = VehicleMode(mode)


def playTune():
    vehicle.play_tune("AAAA")


def parse(msg: str):
    prefix = "cmd: "
    if msg.startswith(prefix):
        return msg.removeprefix(prefix)

    else:
        return None


def on_connect(client, userdata, flags, rc):
    """ Print connection info when connection is established.
    """

    print("Connected with result code "+str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    """ checks if it is a command and executes dronekit command
    """
    print("connected!")
    msg = parse(msg)

    if msg is not None:

        if msg.startswith("setMode"):
            mode = msg.removeprefix("setMode")
            setMode(mode)

        elif msg == "playTune":
            playTune()

        elif msg == "returnHome":
            returnHome()


def main():
    """Create the client connecion to the free broker in HiveMQ and
        receive the ngrok IP published by the Raspberry PI 4"""
    broker = "broker.hivemq.com"
    topic = "bio-optics/bob"
    port = 8884

    client = mqtt.Client()
    client.connect(broker, port)

    client.on_connect = on_connect
    client.on_message = on_message
    print(on_message)

    client.loop_forever()


if __name__ == "__main__":

    while 1:
        try:

            _vehicle_port = '/dev/ttyACM0'
            vehicle = connect(_vehicle_port, baud=115200, heartbeat_timeout=5)

            # get list of waypoints
            cmds = vehicle.commands
            cmds.download()
            cmds.wait_ready()

        except Exception as e:
            print(e)
            print("\n\n retrying in 3 sec...")
            sleep(3)

    main()
