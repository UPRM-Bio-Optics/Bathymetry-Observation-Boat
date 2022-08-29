import socket

sock = socket.socket()
host_ip = socket.gethostbyname()
port = 12354

sock.bind((host_ip, port))
print(f'socket bounded to {port}')