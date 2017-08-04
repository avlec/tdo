import random
import socket
import string
import re


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


def outbound_connection_handler(port, event, handler):
    try:
        print('outbound port is :' + str(port) + '\n')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        s.bind((host, port))
        s.listen(2)
        serversocket,addr = s.accept()
        while not event.is_set:
            msg = handler(port)
            if msg:
                serversocket.send(msg)

    except:
        pass
    event.is_set = True
    serversocket.close()

def command(str,com):
        # regex objects for each command
        for c in com:
            if re.match(com[c], str):
                return True
        return False

def inbound_connection_handler(port,event, handler):
    try:
        print('inbound port is :' + str(port) + '\n')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        addr = (host, port)
        while not event.is_set:

            try:
                s.connect(addr)
                break
            except:
                pass
        while not event.is_set:
            data = s.recv(1024)
            if data:
                handler(data.decode('utf8'))
    except:
        pass
    event.is_set = True
    s.close()


def createID():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
commands = {
    'join': re.compile(r'\/join (\w+)'),
    'create': re.compile(r'\/create (\w+) ?([01]{3})?'),
    'set_alias': re.compile(r'\/set_alias (\w+)'),
    'block': re.compile(r'\/block (\w+)'),
    'unblock': re.compile(r'\/unblock (\w+)'),
    'delete': re.compile(r'\/delete (\w+)'),
    'chmod': re.compile(r'\/chmod (\w+)'),
    'help': re.compile(r'\/help')}

serverCommands = {
    'addUser': re.compile(r'\/addUser (\w+)'),
    'removeUser':re.compile(r'\/removeUser (\w+)'),
    'addChannel': re.compile(r'\/addChannel (\w+)'),
    'removeChannel':re.compile(r'\/removeChannel (\w+)'),
    'loginfailed':re.compile(r'\/duplicateUserAlias'),
    'changealias':re.compile(r'\/changealias (\w+)')}

