import socket
import sys
import threading

def inbound_connection_handler(port):
    print("inbound port is :" + str(port) + "\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = (host, port)
    s.connect(addr)
    while True:
        # Receiving from server
        try:
            data = s.recv(1024)
        except ConnectionResetError:
            print("\nlost connection to server, closing")
            sys.exit()
        if not data:
            break
        print(data.decode())
    s.close()

def outbound_connection_handler(port):
    print("outbound port is :" + str(port) + "\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.bind((host, port))
    s.listen(2)
    serversocket,addr = s.accept()
    while True:
        msg = raw_input('alias:')
        serversocket.send(msg.encode('utf8'))
        # msg = MSG_id + '|' + C.id + '|' +C.currentChannel + '|'+ userinput
        #s.send(msg.encode('utf8'))  
    serversocket.close()

    
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
addr = (host, port)
s.connect(addr)
connection_port = s.recv(1024)
ports = connection_port.decode('utf8').split("|")
p1 = ports.pop()
p2 = ports.pop()
print("my port is " + p1 + " and " + p2)

threading._start_new_thread(inbound_connection_handler, (int(p2),))
threading._start_new_thread(outbound_connection_handler, (int(p1),))
while True:
    pass