import sys
import linuxcnc
import socket

#what: proof of concept CNC server (TCP)
#how: Python 2 *cough* 3
#who: Cayden
#TODO make OOP -> CNC should be a class that holds its connection

def openServer(port=9000): #start up the server, listening on port
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serversocket.bind(('0.0.0.0', port))
    # become a server socket, let only one connection at once
    print(serversocket.getsockname())
    serversocket.listen()
    connection, client_address = serversocket.accept()
    return serversocket, connection, client_address

def connectCNC():
    try:
        s = linuxcnc.stat() # create a connection to the status channel
        return s
    except linuxcnc.error, detail:
        print("error", detail)
        sys.exit(1)

def pollCNC(cnc):
    try:
        cnc.poll() #update status attributes
    except linuxcnc.error, detail:
        print("error", detail)
        sys.exit(1)

def main():
    #open up connection to client listener
    print("Waiting for client to connect...")
    socket, connection, client_address = openServer()
    print("Connected to {}.".format(client_address))

    #open up connection to cnc
    cnc = connectCNC()

    while True:
        pollCNC(cnc)
        position = cnc.actual_position
        connection.sendall(str.encode(str(position)))


if __name__ == "__main__":
    main()
