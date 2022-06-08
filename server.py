import socket
import time


def sock() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    port = 3389
    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen(5)
    print("socket is listening")
    c, addr = s.accept()
    print('Got connection from', addr)
    c.send('Thank you for connecting'.encode())
    message = c.recv(1024).decode()
    c.close()
    return message

if __name__ == '__main__':
  
    while True:
        try:
            message = sock()
        except Exception as e:
            print(f'Exception Occurred: {e}')
            print('Retrying Connection...')
            continue

        f = open("latestIP.txt", "w")
        f.write(message)
        f.close()
        print('Closing')
        time.sleep(100)
    