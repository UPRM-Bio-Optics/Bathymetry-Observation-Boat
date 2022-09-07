import paho.mqtt.client as mqtt
import os
'''
This is the Subscriber and it is used to listen for the ngrok IP published by the RPI on the broker.
Once it receives the IP it attempts to connect via ssh
'''


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("SSH/NCAS-M")


def on_message(client, userdata, msg):
    
    print("Yes!")
    print(msg.payload.decode())
    ip = msg.rsplit("//")[-1]
    try:
        os.system(f"ssh root@{ip}")
    except Exception as err:
        print(err)
    client.disconnect()


if __name__ =="__main__":
    
	client = mqtt.Client()
	client.connect("broker.hivemq.com", 1883)

	client.on_connect = on_connect
	client.on_message = on_message
	print(on_message)

	client.loop_forever()
