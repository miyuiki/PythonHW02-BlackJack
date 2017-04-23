import socket
import sys
import select
import string
 
##player = input("your name : ")

def prompt() :
    sys.stdout.flush()

#main function
if __name__ == "__main__":
	
 
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()
 
    host = sys.argv[1]
    port = int(sys.argv[2])
 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
 
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
 	
    print 'Connected to remote host.'
    prompt()
 
    while 1:
        socket_list = [sys.stdin, s]
 
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
 
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from game server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()
 
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg[0])
                prompt()