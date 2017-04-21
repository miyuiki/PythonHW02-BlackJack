import socket
import select
import random

card = []
for i in xrange(1,5):
    for j in xrange(1,14):
        card.append((i,j))
def get_card(card):
    rand = random.randint(1, len(card)+1)
    content = card[rand]
    card.remove(content)
    return content
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        try:
            socket.send(message)
        except :
            pass
 
if __name__ == "__main__":
    houseman = []
    player = []

    houseman.append(get_card(card))
    houseman.append(get_card(card))
    
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(5)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Game server started on port " + str(PORT) + " waiting for player..."
    print "card1: " + str(houseman[0]) + " card2: " + str(houseman[1])
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Player (%s, %s) connected" % addr
 
                broadcast_data(sockfd, "[%s:%s] join the game\n" % addr)
                broadcast_data(sock, "house man: %s\n" %str(houseman[0]))
 
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "r" + ' ' + data)                
 
                except:
                    broadcast_data(sock, "PLayer (%s, %s) is offline" % addr)
                    print "Player (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue