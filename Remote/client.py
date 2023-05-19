import requests
import json
import time
import subprocess
import paho.mqtt.client as mqtt


def getNgrok():
    '''subprocess.Popen(["ngrok","tcp", "22"],
                        stdout=subprocess.PIPE)'''

    time.sleep(3)  # to allow the ngrok to fetch the url from the server
    localhost_url = "http://localhost:4040/api/tunnels"  # Url with tunnel details
    tunnel_url = requests.get(localhost_url).text  # Get the tunnel information
    j = json.loads(tunnel_url)

    tunnel_url = j['tunnels'][0]['public_url']  # Do the parsing of the get
    print(tunnel_url)
    return tunnel_url.encode()


def on_publish(client, userdata, result):
    print("Data Published dickface!")
    pass


def main():

    # This is the Publisher

    client = mqtt.Client()
    client.on_publish = on_publish
    hiveMQ = "broker.hivemq.com"
    client.connect(hiveMQ, 1883)
    message = getNgrok()
    client.publish("bio-optics/bob", message)
    client.disconnect()


if __name__ == '__main__':
    main()