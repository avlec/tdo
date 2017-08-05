import random
import socket
import string
import sys
import threading
import CommonUtil
import functools
import time
import re
from messages.Message import Message as Message
from database.databaseinterface import databaseinterface

# Globals
db = databaseinterface()

def welcome_message():
    msg = Message('0000000000000000', '0000000000000000', 'server', 'welcome to TDO communication services')
    return msg


class User:
    def __init__(self, alias, userID, inport,outport):
        self.alias = alias
        self.id = userID
        self.password = None
        self.inport = inport
        self.outport = outport
        self.channels = []
        db.new_user(self)

    @staticmethod
    def newUser(alias, inport, outport):
        user = db.get_user_from_alias(alias)
        print user
        if user is None:
            return User(alias, CommonUtil.createID(), inport, outport)
        else:
            return User(user[0], user[1], inport, outport)

    @staticmethod
    def getUser(users, userID):
        for u in users:
            if u.id == userID:
                return u
        return None


class Channel:
    def __init__(self, name, permissions, channelID = None):
        ch = db.get_channel_from_name(name)
        if ch is None:
            self.id = CommonUtil.createID()
            self.name = name
            self.blockedUsers = []
        else:
            (self.id,
             self.name,
             self.permissions,
             self.blockedUsers) = ch
        self.admin = []
        self.users = []
        self.permissions = permissions

    @staticmethod
    def getUser(channels,userid):
        for ch in channels:
            for u in ch.users:
                if u.id ==userid:
                    return u

    @staticmethod
    def getChannel(channels, channelName):
        for ch in channels:
            if ch.name == channelName:
                return ch
        return None

    @staticmethod
    def getUserChannel(channels,userID):
        for ch in channels:
            for u in ch.users:
                if u.id == userID:
                    return u
        return None

    @staticmethod
    def getUserAliasChannel(channels,userAlias):
        for ch in channels:
            for u in ch.users:
                if u:
                    if u.alias == userAlias:
                        return u
        return None


    @staticmethod
    def getChannelWithUser(channels,userid):
        for ch in channels:
            for u in ch.users:
                if userid == u.id:
                    return ch
        return None


    @staticmethod
    def removeChannel(channels, channelID):
        ch = Channel.getChannel(channels, channelID)
        channels.remove(ch)
        # Delete channel from DB
        db.delete_channel(ch)

    @staticmethod
    def moveUser(channels, channel, userid):
        for ch in channels:
            for u in ch.users:
                if u.id == userid:
                    ch.users.remove(u)
                    channel.users.append(u)
                    return None

    @staticmethod
    def removeUser(channels, user):
        for ch in channels:
            if user in ch.users:
                ch.users.remove(user)
                return

# ----------------------------------------------------------------------------------------------------------------------------------
# Server class and subclasses
# ----------------------------------------------------------------------------------------------------------------------------------

class Server:
    def __init__(self):
        self.Outbound = {}
        self.connections = {}
        self.Inbound = CommonUtil.Queue()
        self.Error = CommonUtil.Queue()
        self.Channels = []
        self.general = Channel('General', '011', '0000000000000000')
        self.Channels.append(self.general)
        self.handler = self.PortHandler()
        self.users = []


    class PortHandler:
        def __init__(self):
            self.port = []
            for i in range(20000, 10000, -1):
                self.port.append(i)

    # handler method for outbound connections
    @staticmethod
    def send(s, p):
        msg = s.Outbound[p].Pop()
        if msg:
            print msg.message
            return msg.encode()
            
    @staticmethod
    def error():
        print('user left channel')

    # handler method for inbound connections
    def enqueue(self, p, d):

        def validate(d):
            pass

        validate(d)
        msg = Message.decode(d)
        self.Inbound.Push(msg)

    def SendCommand(self, msg):
        print msg.message
        for ch in self.Channels:
            for u in ch.users:
                self.Outbound[u.inport].Push(msg)

    def dequeue(self):
        while True:
            c = self.connections.copy()
            for u in c:
                if self.connections[u].is_set:
                    Channel.removeUser(self.Channels, u)
                    com = '/removeUser '+u.alias
                    m = Message(0000000000000000, 0000000000000000, 'server', com)
                    self.SendCommand(m)
                    self.connections.pop(u)
                    self.handler.port.append(u.inport)
                    self.handler.port.append(u.outport)
                    break
            msg = self.Inbound.Pop()

            if msg:  # pop returns none if nothing is on que, not entering processing
                if CommonUtil.command(msg.message,CommonUtil.commands):  # checking if message is a command
                    # for loop runs over every command type, only one matches, running inner if  once for processing
                    for command in CommonUtil.commands:
                        regex = re.match(CommonUtil.commands[command], msg.message)
                        if regex:
                            if command == 'join':
                                ch = Channel.getChannel(self.Channels, regex.group(1))
                                u = Channel.getUser(self.Channels,msg.messageSenderId)
                                if ch:
                                    if u not in ch.blockedUsers:
                                        ch.moveUser(self.Channels, ch, msg.messageSenderId)
                                        msg = Message(0000000000000000, 0000000000000000, 'server', 'user:'+Channel.getUser(self.Channels,msg.messageSenderId).alias+' joined the channel')
                                        for u in ch.users:
                                            if u.id != msg.messageSenderId:
                                                self.Outbound[u.inport].Push(msg)
                                    else:
                                        errMsg = Message(0000000000000000, 0000000000000000, 'server', 'you are blocked from this channel')
                                        self.Outbound[u.inport].Push(errMsg)
                                else:
                                    errMsg = Message(0000000000000000, 0000000000000000, 'server', 'channel not found')
                                    self.Outbound[u.inport].Push(errMsg)
                            if command == 'create':
                                ch = Channel.getChannel(self.Channels, regex.group(1))
                                u = Channel.getUser(self.Channels, msg.messageSenderId)
                                if ch or not u:
                                    u = Channel.getUser(self.Channels, msg.messageSenderId)
                                    helpMsg = Message(0000000000000000, 0000000000000000, 'server', 'channel with that name exists')
                                    self.Outbound[u.inport].Push(helpMsg)
                                else:
                                    ch = Channel(regex.group(1), regex.group(2))
                                    ch.admin.append(u)
                                    self.Channels.append(ch)
                                    com = '/addChannel '+regex.group(1)
                                    m = Message(0000000000000000, 0000000000000000, 'server', com)
                                    self.SendCommand(m)
                                ch.moveUser(self.Channels, ch, msg.messageSenderId)
                            if command == 'set_alias':
                                u = Channel.getUserAliasChannel(self.Channels,regex.group(1))
                                if u:
                                    u = Channel.getUser(self.Channels, msg.messageSenderId)
                                    errMsg = Message(0000000000000000, 0000000000000000, 'server', 'user with that alias exists')
                                    server.Outbound[u.inport].Push(errMsg)
                                else:
                                    u = Channel.getUser(self.Channels, msg.messageSenderId)
                                    if u:
                                        com = Message(0000000000000000, 0000000000000000, 'server', '/removeUser '+u.alias)
                                        self.SendCommand(com)
                                        u.alias = regex.group(1)
                                        com = Message(0000000000000000, 0000000000000000, 'server', '/changealias '+regex.group(1))
                                        server.Outbound[u.inport].Push(com)
                                        com = Message(0000000000000000, 0000000000000000, 'server', '/addUser '+regex.group(1))
                                        self.SendCommand(com)

                            if command == 'delete':
                                ch = Channel.getChannel(self.Channels, regex.group(1))
                                u = Channel.getUser(self.Channels, msg.messageSenderId)
                                if ch:
                                    if u in ch.admin:
                                        self.general.users.extend(ch.users)
                                        self.Channels.remove(ch)
                                        m = Message(0000000000000000, 0000000000000000, 'server', 'channel ' + regex.group(1)+ ' deleted')
                                        for u in ch.users:
                                            self.Outbound[u.inport].Push(m)
                                        com = '/removeChannel '+regex.group(1)
                                        m = Message(0000000000000000, 0000000000000000, 'server', com)
                                        self.SendCommand(m)
                                    else:
                                        errMsg = Message(0000000000000000, 0000000000000000, 'server', 'insufficient permissions')
                                        self.Outbound[u.inport].Push(errMsg)


                            if command == 'chmod':
                                admin = Channel.getUser(self.Channels, msg.messageSenderId)
                                u = Channel.getUser(self.Channels, regex.group(1))
                                ch = Channel.getChannelWithUser(self.Channels, msg.messageSenderId)
                                if ch:
                                    if admin in ch.admin:
                                        ch.admin.append(u)
                                    else:
                                        errMsg = Message(0000000000000000, 0000000000000000, 'server', 'insufficient permissions')
                                        self.Outbound[admin.inport].Push(errMsg)
                            if command == 'block':
                                admin = Channel.getUser(self.Channels, msg.messageSenderId)
                                u = Channel.getUserAliasChannel(self.Channels, regex.group(1))
                                ch = Channel.getChannelWithUser(self.Channels, msg.messageSenderId)
                                if ch:
                                    if admin in ch.admin:
                                        if u:
                                            if u not in ch.blockedUsers:
                                                ch.blockedUsers.append(u)
                                                Channel.moveUser(self.Channels, self.general, u.id)
                                                print 'llllllll'
                                            else:
                                                errMsg = Message(0000000000000000, 0000000000000000, 'server', 'user is already blocked')
                                                self.Outbound[admin.inport].Push(errMsg)
                                        else:
                                            errMsg = Message(0000000000000000, 0000000000000000, 'server', 'user not found')
                                            self.Outbound[admin.inport].Push(errMsg)
                                    else:
                                        if u:
                                            errMsg = Message(0000000000000000, 0000000000000000, 'server', 'insufficient permissions')
                                            self.Outbound[admin.inport].Push(errMsg)
                                        else:
                                            errMsg = Message(0000000000000000, 0000000000000000, 'server', 'user not found')
                                            self.Outbound[admin.inport].Push(errMsg)
                            if command == 'unblock':
                                admin = Channel.getUser(self.Channels, msg.messageSenderId)
                                u = Channel.getUser(self.Channels, regex.group(1))
                                ch = Channel.getChannelWithUser(self.Channels, msg.messageSenderId)
                                if ch:
                                    if admin in ch.admin:
                                        if u:
                                            if u in ch.blockedUsers:
                                                ch.blockedUsers.remove(u)
                                            else:
                                                errMsg = Message(0000000000000000, 0000000000000000, 'server', 'user is already not blocked')
                                                self.Outbound[admin.inport].Push(errMsg)
                                        else:
                                            errMsg = Message(0000000000000000, 0000000000000000, 'server', 'user not found')
                                            self.Outbound[admin.inport].Push(errMsg)
                                    else:
                                        errMsg = Message(0000000000000000, 0000000000000000, 'server', 'insufficient permissions')
                                        self.Outbound[admin.inport].Push(errMsg)

                            if command == 'help':
                                u = Channel.getUser(self.Channels, msg.messageSenderId)
                                s = 'hi'
                                helpMsg = Message(0000000000000000, 0000000000000000, 'server', s)
                                server.Outbound[u.inport].Push(helpMsg)

                else:
                    msg.senderAlias = Channel.getUser(self.Channels, msg.messageSenderId).alias
                    ch = Channel.getChannelWithUser(self.Channels, msg.messageSenderId)
                    print(ch.name + '|' + msg.messageSenderId + ":" + msg.message)
                    if ch:
                        for u in ch.users:
                            if u.id != msg.messageSenderId:
                                self.Outbound[u.inport].Push(msg)


if __name__ == '__main__':
    server = Server()
    dequeue = threading.Thread(target=server.dequeue, args=())
    dequeue.start()
    # setting up port for connecting to clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    server_socket.bind((host, port))
    server_socket.listen(10)
    # while loop for handling new connections
    while True:
        clientsocket, addr = server_socket.accept()
        print('Got a connection from %s' % str(addr))
        p1 = server.handler.port.pop()
        p2 = server.handler.port.pop()
        server.Outbound[p1] = CommonUtil.Queue()
        server.Outbound[p1].Push(welcome_message())
        alias = clientsocket.recv(1024)
        if Channel.getUserAliasChannel(server.Channels, alias):
            print('duplicate user')
            alias = 'bob'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            m = Message(0000000000000000, 0000000000000000, 'server', 'alias was taken, you have received '+ alias+' instead, to change use /set_alias')
            server.Outbound[p1].Push(m)
        newUser = User.newUser(alias, p1, p2)
        server.general.users.append(newUser)
        # sending the client the information on ports used
        k = str(p1)+'|'+str(p2)+'|'+newUser.id
        clientsocket.send(k.encode('utf8'))


        for ch in server.Channels:
            com = '/addChannel '+ch.name
            m = Message(0000000000000000, 0000000000000000, 'server', com)
            server.Outbound[p1].Push(m)
            for u in ch.users:
                if u.alias != alias:
                    com = '/addUser '+u.alias
                    m = Message(0000000000000000, 0000000000000000, 'server', com)
                    server.Outbound[p1].Push(m)


        com = '/addUser '+alias
        m = Message(0000000000000000, 0000000000000000, 'server', com)
        server.SendCommand(m)
        clientsocket.close()
        event = threading.Event()
        event.is_set = False
        server.connections[newUser] = event
        outbound = threading.Thread(target=CommonUtil.outbound_connection_handler, args=(p1, event, functools.partial(server.send, server)),)
        inbound = threading.Thread(target=CommonUtil.inbound_connection_handler, args=(p2, event, functools.partial(server.enqueue, server)),)
        # starting threads to manage connection
        outbound.start()
        time.sleep(0.05)
        inbound.start()
