import socket
import sys
import threading
import CommonUtil
import functools
import time
from messages.Message import Message as Message


def welcome_message():
    msg = Message('0000000000000000', '0000000000000000', 'server', '0000000000000000', "welcome to TDO communication services")
    return msg


class user:
    def __init__(self, alias, userid, inport,outport):
        self.alias = alias
        self.id = userid
        self.inport = inport
        self.outport = outport
        self.password ='password123'
        self.currentchannel='0000000000000000'

# todo implement DB connection
class Channel:
    @staticmethod
    def is_permissions(permissions):
        if permissions:
            return True
        elif False:  # insert regex to check that its a bitstring length 3
            pass
        else:
            return False

    def __init__(self, name, permissions):
        self.name = name
        if name == 'General':
            self.id = '0000000000000000'
        else:
            self.id = CommonUtil.createID()

        #users should be a table in future
        self.users = []
        if self.is_permissions(permissions):
            self.default_permissions = permissions
        else:
            self.default_permissions = '011'

    def change_default_permisions(self, permissions):
        if self.is_permissions(permissions):
            self.default_permissions = permissions
        else:
            pass

    def add_user(self, user):
        self.users.append(user)


# ----------------------------------------------------------------------------------------------------------------------------------
# Server class and subclasses
# ----------------------------------------------------------------------------------------------------------------------------------

class Server:
    def __init__(self):
        self.Outbound = {}
        self.Inbound = CommonUtil.Queue()
        self.Error = CommonUtil.Queue()
        self.Channels = []
        self.Channels.append(Channel('General', '011'))
        self.handler = self.PortHandler()
        self.users = []
    class PortHandler:
        def __init__(self):
            self.port = []
            for i in range(20000, 10000, -1):
                self.port.append(i)

    @staticmethod
    def send(s, p):
        msg = s.Outbound[p].Pop()
        if msg:
            return msg.data

    def enqueue(self, p, d):
        def validate(d):
            pass

        def enqueue(self, message):
            self.Inbound.Push(message)

        def dequeue(self):
            msg = self.Inbound.Pop()
            for u in self.users:
                if u.id != msg.messageSenderId and u.currentchannel == msg.messageChannelId:
                    self.Outbound[u.inport].Push(msg)


        validate(d)
        msg = Message(d)
        enqueue(self, msg)
        dequeue(self)  # temp method, will move somewhere, do it independently on a loop in thread


if __name__ == '__main__':
    server = Server()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    server_socket.bind((host, port))
    server_socket.listen(10)
    while True:
        clientsocket, addr = server_socket.accept()
        print('Got a connection from %s' % str(addr))
        p1 = server.handler.port.pop()
        p2 = server.handler.port.pop()
        newuserid=CommonUtil.createID()

        # sending the client the information on ports used
        k = str(newuserid) + '|' + str(p1)+'|'+str(p2)
        clientsocket.send(k.encode('utf8'))
        # starting threads to manage connection
        server.Outbound[p1] = CommonUtil.Queue()
        server.Outbound[p1].Push(welcome_message())
        server.users.append(user('', newuserid, p1, p2))
        threading._start_new_thread(CommonUtil.outbound_connection_handler, (p1, functools.partial(server.send, server),))
        time.sleep(0.05)
        threading._start_new_thread(CommonUtil.inbound_connection_handler, (p2, functools.partial(server.enqueue, server),))
        clientsocket.close()
