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

    print("Got a connection fromm %s" %str(addr))
    current = time.ctime(time.time()) + "\r\n"
    client.send(current.encode('ascii'))

    client.close()