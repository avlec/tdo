import random
import socket
import string


# ----------------------------------------------------------------------------------------------------------------------------------
# utility classes, Message, Queue, connection error
# ----------------------------------------------------------------------------------------------------------------------------------

# Queue class used for storing messages during processing.
class Queue:
    def __init__(self):
        self.messages = []

    def Pop(self):
        if len(self.messages) > 0:
            return self.messages.pop(0)

    def Push(self, message):
        self.messages.append(message)

class connection_error(Exception):

    def __init__(self, msg):
        self.expr = 'connection error'
        self.msg = msg

# ----------------------------------------------------------------------------------------------------------------------------------
# end of utility classes
# ----------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------
# Utility functions: connection handlers
# ----------------------------------------------------------------------------------------------------------------------------------


def outbound_connection_handler(port, handler):
    print('outbound port is :' + str(port) + '\n')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.bind((host, port))
    s.listen(2)
    serversocket,addr = s.accept()
    while True:
        msg = handler(port)
        if msg:
            serversocket.send(msg)
    serversocket.close()


def inbound_connection_handler(port, handler):
    print('inbound port is :' + str(port) + '\n')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = (host, port)
    s.connect(addr)
    while True:
        data = s.recv(1024)
        if not data:
            raise connection_error('invalid data')
        print(data.decode('utf8'))
        handler(data.decode('utf8'))
    s.close()


def createID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


