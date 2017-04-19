import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Create socket")
host = socket.gethostname()
port = 9999

server.bind((host,port))
server.listen(5)
while True:
    client,addr = server.accept()

    print("Got a connection by %s" %str(addr))
    data = client.recv(1024)
    if not data:
    	break
    client.sendall(data)
    print("received message %s" %str(data))
client.close()