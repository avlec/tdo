import socket
import time
import threading


class PortHandler:
    def __init__(self):
        self.port = []
        for i in range(20000, 10000, -1):
            self.port.append(i)


def inbound_connection_handler(port):
    print("inbound port is :" + str(port) + "\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = (host, port)
    s.connect(addr)
    while True:
        # Receiving from client
        try:
            data = s.recv(1024)
        except socket.error:
            print("user " + str(port) + " disconnected")
            break
        if not data:
            break
        # insert command parser here and check if the client sent command
        print (str(port)+":"+data.decode())
        # add timeout in 10 mins?
    s.close()
    

def outbound_connection_handler(port):
    print("outbound port is :" + str(port) + "\n")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server_socket.bind((host, port))
    server_socket.listen(2)
    while True:
        clientsocket,addr = server_socket.accept()
        welcome = "welcome to TDO communication server"
        clientsocket.send(welcome.encode('utf8'))
    clientsocket.close()


handler = PortHandler()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
server_socket.bind((host, port))
server_socket.listen(10)
while True:
    clientsocket,addr = server_socket.accept()
    print("Got a connection from %s" % str(addr))
    p1 = handler.port.pop()
    p2 = handler.port.pop()
    # sending the client the information on ports used
    k =str(p1)+"|"+str(p2)
    clientsocket.send(k.encode('utf8'))

    # starting threads to manage connection
    
    threading._start_new_thread(outbound_connection_handler, (p1,))
    threading._start_new_thread(inbound_connection_handler, (p2,))

    clientsocket.close()