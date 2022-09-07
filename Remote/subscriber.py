import paho.mqtt.client as mqtt
import os 
# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("SSH/NCAS-M")

def on_message(client, userdata, msg):
    print("Yes!")
    print(msg.payload.decode())
    ip = msg.rsplit("//")[-1]
    os.system(f"ssh root@{ip}")
    client.disconnect()
    
client = mqtt.Client()
client.connect("broker.hivemq.com",1883)

client.on_connect = on_connect
client.on_message = on_message
print(on_message)

client.loop_forever()