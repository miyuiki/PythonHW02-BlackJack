import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created!")

host = socket.gethostname()
port = 9999

client.connect((host,port))
while True:
	msg = input("send some message: ")
	client.sendall(str(msg))
	recv_data = client.recv(1024)
	
	print("echo from server is %s" % repr(recv_data))
client.close()