import socket
import select
import sys

HOST = ''
PORT = 9999
RECV_BUFFER = 4096
socket_list = []

def BJ_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10)
    socket_list.append(server_socket)

    print ("server socket start on port" + str(PORT))
    while True:
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)
        for sock in ready_to_read:
            if socket == server_socket:  # new connection
                socket_fd, adr = server_socket.accept()
                socket_list.append(socket_fd)
                print ("Client (%s,%s) connect" % adr)

                broadcast(server_socket, socket_fd, "[%s:%s] entered game\n" % adr)
            else:  # message from client
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast(server_socket,sock,"\r"+'['+str(sock.getpeername())+']'+data)
                    else:
                        if sock in socket_list:
                            socket_list.remove(sock)
                        broadcast(server_socket,sock,"Client (%s,%s) is offline\n" % adr)
                except:
                    broadcast(server_socket, sock, "Client (%s,%s) is offline\n" % adr)
                    continue
        server_socket.close()
def broadcast(server_socket,sock,msg):
    for socket in socket_list:
        if socket != server_socket and socket != sock:
            try:
                socket.send(msg)
            except:
                socket.close()
                if socket in socket_list:
                    socket_list.remove(socket)

if __name__ == '__main__':
    sys.exit(BJ_server())