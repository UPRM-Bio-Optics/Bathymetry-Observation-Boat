import paho.mqtt.client as mqtt
import os
'''
This is the Subscriber and it is used to listen for the ngrok IP published by the RPI on the broker.
Once it receives the IP it attempts to connect via ssh
'''


def on_connect(client, userdata, flags, rc):
    """ Print connection info when connection is established.
    """
    print("Connected with result code "+str(rc))
    client.subscribe("SSH/NCAS-M")


def on_message(client, userdata, msg):
    """Once connected, this function decodes ngrok IP adress and attempts to ssh in local terminal.
    """
    print("Connected!\n")
    print(f"ngrok IP: {msg.payload.decode()}\n")

    ip = msg.payload.decode().rsplit("//")[-1]
    ip, port = ip.rsplit(":")
    try:
        os.system(f"ssh root@{ip} -p {port}")
    except Exception as err:
        print(err)
    client.disconnect()

def main():
    """Create the client connecion to the free broker in HiveMQ and 
        receive the ngrok IP published by the Raspberry PI 4"""
    client = mqtt.Client()
    client.connect("broker.hivemq.com", 1883)

    client.on_connect = on_connect
    client.on_message = on_message
    print(on_message)

    client.loop_forever()
    
    
if __name__ == "__main__":
    main()