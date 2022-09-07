import paho.mqtt.client as mqtt

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("SSH/NCAS-M")

def on_message(client, userdata, msg):
    print("Yes!")
    print(msg.payload.decode())
    client.disconnect()
    
client = mqtt.Client()
client.connect("broker.hivemq.com",1883)

client.on_connect = on_connect
client.on_message = on_message
print(on_message)

client.loop_forever()