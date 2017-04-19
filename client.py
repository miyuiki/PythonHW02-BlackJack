import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created!")

host = socket.gethostname()
port = 9999

client.connect((host,port))
tm = client.recv(1024)

client.close()
print("time receive from server is %s" % tm.decode('ascii'))