import subprocess
import requests
import json
import time
import socket

def main():
    subprocess.Popen("ngrok tcp 22",
                    stdout=subprocess.PIPE)

    
    time.sleep(3) # to allow the ngrok to fetch the url from the server
    localhost_url = "http://localhost:4040/api/tunnels" #Url with tunnel details
    tunnel_url = requests.get(localhost_url).text #Get the tunnel information
    j = json.loads(tunnel_url)

    tunnel_url = j['tunnels'][0]['public_url'] #Do the parsing of the get
    print(tunnel_url)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 3389
    print("Trying to connect...")
    s.connect(('34.95.19.212', port))
    print(s.recv(1024).decode())
    s.sendall(tunnel_url.encode())
    s.close()
    
    
if __name__ == '__main__':
    main()
