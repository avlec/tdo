import socket
import sys
import threading


def inbound_connection_handler(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = (host, port)
    s.connect(addr)
    s.bind(addr)
    s.listen(2)
    while True:
        # Receiving from client
        try:
            data = s.recv(1024)
        except ConnectionResetError:
            print("\nlost connection to server, closing")
            sys.exit()
        if not data:
            break
        print(data.decode())
    s.close()


def outbound_connection_handler():

    pass


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
s.connect((host, port))
connection_port = s.recv(1024)
ports = connection_port.decode('ascii').split("|")
p1 = ports.pop()
p2 = ports.pop()
print("my port is " + p1 + " and " + p2)
threading._start_new_thread(inbound_connection_handler, (int(p2),))
outbound = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
outbound.connect((host, port))
while False:#change to true, when functionality used
        msg = input('alias:')
        MSG_id = Connector.createID()
        #msg = MSG_id + '|' + C.id + '|' +C.currentChannel + '|'+ msg
        msg = bytes(msg, encoding='utf8')
        outbound.send(msg)