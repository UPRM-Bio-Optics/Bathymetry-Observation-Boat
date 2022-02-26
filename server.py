import socket
import time
while True:
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
    port = 3389
    s.bind(('', port))
    print ("socket binded to %s" %(port))
    s.listen(5)
    print ("socket is listening")
    c, addr = s.accept()
    print ('Got connection from', addr )
    c.send('Thank you for connecting'.encode())
    message = c.recv(1024).decode()
    f = open("latestIP.txt", "w")
    f.write(message)
    f.close()
    print("Closing")
    c.close()
    time.sleep(100)
  except KeyboardInterrupt:
    break
  except:
    continue


