import socket
import select
import random

import sys

burst = 0
no = 0
win = 0

card = []
houseman = []
player = [[], [], [], [], []]  # 5 player's card
final_point = [] #player's point and houseman's point

for i in xrange(1, 5):
    for j in xrange(1, 14):
        card.append((i, j))


def get_card(card):
    rand = random.randint(1, len(card))
    content = card[rand - 1]
    card.remove(content)
    return content


# Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message):
    # Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        try:
            socket.send(message)
        except:
            pass


def broadcast_player(sock, message):
    for socket in CONNECTION_LIST:
        if socket == sock:
            try:
                socket.send(message)
            except:
                pass


def calculate(card):
    kc = 0
    qc = 0
    jc = 0
    ac = 0
    point = 0

    for x in xrange(0, len(card)):
        point += card[x][1]

        if card[x][1] == 13:
            kc += 1
        elif card[x][1] == 12:
            qc += 1
        elif card[x][1] == 11:
            jc += 1
        elif card[x][1] == 1:
            ac += 1
    point = point - 3 * kc - 2 * qc - jc + 9 * ac
    if ac > 0 and point > 21:
        cnt = ac
        while point > 21 and cnt != 0:
            point = point - 9
            cnt = cnt - 1

    return point


def ask(data, player, toplayer, clist):
    global burst
    global no
    global win

    if data == 'y':
        player.append(get_card(card))

        if calculate(player) > 21:
            broadcast_player(toplayer, str(player) + "\npoint: " + str(calculate(player)) + "\nYou lose :(\n")
            toplayer.close()
            CONNECTION_LIST.remove(toplayer)
            final_point.append(0) #burst, append 0 instead of point
            del player[:]


        elif calculate(player) == 21:
            broadcast_player(toplayer, str(player) + "\npoint: " + str(calculate(player)))
            final_point.append(calculate(player))
            del player[:]
            win += 1


        else:
            broadcast_player(toplayer, str(player) + "\npoint: " + str(calculate(player)) + "\nmore card? (y/n)\n")

    elif data == 'n':
        if len(clist) > 2:
            broadcast_player(toplayer, str(player) + "\nTotal point: " + str(calculate(player)) + "\nPlease wait for other players.\n")
        else:
            broadcast_player(toplayer, str(player) + "\nTotal point: " + str(calculate(player)) + "\nPlease wait for houseman\n")
        final_point.append(calculate(player))
        del player[:]
        no += 1


    else:
        broadcast_player(toplayer, "Check your answer")


if __name__ == "__main__":


    index = 0

    houseman.append(get_card(card))
    houseman.append(get_card(card))

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(5)

    # Add server socket to the jlist of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Game server started on port " + str(PORT) + " waiting for player..."
    print "card1: " + str(houseman[0]) + " card2: " + str(houseman[1])

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Player (%s, %s) connected" % addr
                index = CONNECTION_LIST.index(sockfd)

                player[index].append(get_card(card))
                player[index].append(get_card(card))

                broadcast_data(sockfd, "[%s:%s] join the game\n" % addr)
                broadcast_player(sockfd, "house man: %s\n" % str(houseman[0]))
                broadcast_player(sockfd, "your card: %s\nmore card?(y/n)\n" % (str(player[index])))

            # Some incoming message from a clientm
            else:
                index = CONNECTION_LIST.index(sock)
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        ask(str(data), player[index], sock, CONNECTION_LIST)
                        if burst + no + win == len(CONNECTION_LIST)-1:
                            print("houseman's turn")
                            while calculate(houseman) < 17:
                                houseman.append(get_card(card))
                            print (str(houseman) + "Your point: " + str(calculate(houseman)))
                            if calculate(houseman) > 21:
                                for x in xrange(0, len(final_point)):
                                    flag = cmp(calculate(houseman), final_point[x])
                                    if final_point[x] <= 21:
                                        print "You lose player %s\n" % str(x+1)
                                        broadcast_data(sock,
                                                       str(houseman) + "Houseman's point: " + str(calculate(houseman)) +
                                                       "\nPLayer %s win\n" % str(x+1))

                                    else:
                                        print "You win player %s\n" % str(x+1)
                                        broadcast_data(sock,
                                                       str(houseman) + "Houseman's point: " + str(calculate(houseman)) +
                                                       "\nPLayer %s lose\n" % str(x+1))


                            elif calculate(houseman) == 21:
                                for x in xrange(0, len(final_point)):
                                    if final_point[x] == 21:
                                        print "Tie with player %s" % str(x+1)
                                        broadcast_data(sock,
                                                       str(houseman) + "Houseman's point: " + str(calculate(houseman)) +
                                                       "\nPLayer %s tie with houseman\n" %str(x+1))

                                    else:
                                        print "You win player %s" % str(x+1)
                                        broadcast_data(sock,
                                                       str(houseman) + "Houseman's point: " + str(calculate(houseman)) +
                                                       "\nPLayer %s lose\n" % str(x+1))

                            else:
                                for x in xrange(0, len(final_point)):
                                    flag = cmp(calculate(houseman), final_point[x])
                                    if flag < 0:
                                        print "You lose player %s" % str(x+1)
                                        broadcast_data(sock,
                                                       str(houseman) + "Houseman's point: " + str(calculate(houseman)) +
                                                       "\nPLayer %s win\n" % str(x+1))

                                    else:
                                        print "You win player %s" % str(x+1)
                                        broadcast_data(sock,
                                                       str(houseman) + "Houseman's point: " + str(calculate(houseman)) +
                                                       "\nPLayer %s lose\n" % str(x+1))
                except:
                    pass
