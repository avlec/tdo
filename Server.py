import socket
import sys
import threading
import CommonUtil
import functools
import time
import re
from messages.Message import Message as Message


def welcome_message():
    msg = Message('0000000000000000', '0000000000000000', 'server', '0000000000000000', 'welcome to TDO communication services','message')
    return msg
class db:
    @staticmethod
    def getUser(userid):
        pass
    @staticmethod
    def userHasPermisions(user,permisions):
        pass
    @staticmethod
    def change_default_permisions(channel, permissions):
        regex = re.match(r'([01]{3})',permissions)
        if regex:
            pass#change permision
    @staticmethod
    def getChannel(server,channel):
        for ch in server.Channels:
            if ch.name == channel:
                return ch
        return None

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
    def __init__(self, name, permissions):
        self.name = name
        if name == 'General':
            self.id = '0000000000000000'
        else:
            self.id = CommonUtil.createID()
        regex = re.match(r'([01]{3})', permissions)
        if regex:
           self.permisions = permissions
        else:
            self.permisions = '011'


    def addUser(self, user):
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
            return msg.encode()

    def enqueue(self, p, d):

        def validate(d):
            pass

        def enqueue(self, message):
            self.Inbound.Push(message)
        #will get moved to seperate thread soon TM
        def dequeue(self):
            msg = self.Inbound.Pop()
            if msg.messageType == 'command':
                for command in CommonUtil.commands:
                    regex = re.match(CommonUtil.commands[command], msg.message)
                    if regex:
                        if command == 'join':
                            ch =db.getChannel(self, regex.group(0))
                            if ch:
                                ch.addUser(db.getUser(msg.messageSenderId))
                        if command == 'create':
                            ch = db.getChannel(self, regex.group(0))
                            if ch:
                                pass#send user error msg
                            else:
                                c = Channel(regex.group(0), regex.group(1))
                                self.Channels.append(c)
                                c.addUser(db.getUser(msg.messageSenderId))
                        if command == 'set_alias':
                            pass#check existance, then create or send msg
                        if command == 'block':
                            pass#check permision, existance, then create or send msg
                        if command == 'unblock':
                            pass#check permision, existance, then create or send msg
                        if command == 'delete':
                            pass#check permision, then create or send msg
                        if command == 'chmod':
                            pass#check permision, existance, then chmod or send msg

                    else:
                        pass# respond with channel not found?

            else:
                print(msg.message)
                for u in self.users:
                    if u.id != msg.messageSenderId and u.currentchannel == msg.messageChannelId:
                        self.Outbound[u.inport].Push(msg)


        validate(d)
        msg = Message.decode(d)
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
