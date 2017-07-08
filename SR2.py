import socket
import time
import threading
import CONN2

class PortHandler:
    def __init__(self):
        self.port = []
        for i in range(20000, 10000, -1):
            self.port.append(i)

def inbound_connection_handler(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = (host, port)
    s.connect(addr)
    s.bind(addr)
    s.listen(3)
    while True:
        # Receiving from client
        data = s.recv(1024)
        if not data:
            break
        # insert command parser here and check if the client sent command
        print (data.decode())
        # add timeout in 10 mins?
    s.close()

def outbound_connection_handler(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = (host, port)
    s.connect(addr)
    while True:
        msg = input('alias:')
        # encodes message
        # msg = MSG_id + '|' + C.id + '|' +C.currentChannel + '|'+ userinput
        msg = bytes(msg, encoding='utf8')
        s.send(msg)
        print("hello")


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
    clientsocket.send(k.encode('ascii'))

    #starting threads to manage connection
    #threading._start_new_thread(outbound_connection_handler, (p1,))
    #threading._start_new_thread(inbound_connection_handler, (p2,))


    clientsocket.close()