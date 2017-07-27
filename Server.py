import socket
import sys
import threading
import CommonUtil
import functools
import time
import re
from messages.Message import Message as Message
from database.databaseinterface import databaseinterface
#welcom message sent to every user apon login
def welcome_message():
    msg = Message('0000000000000000', '0000000000000000', 'server', '0000000000000000', 'welcome to TDO communication services','message')
    return msg

db = databaseinterface()


class User:
    def __init__(self, alias, userid, inport,outport):
        self.alias = alias
        self.id = userid
        self.inport = inport
        self.outport = outport
        self.password ='password123'
        self.currentchannel='0000000000000000'
        self.channels = []
        self.blockedChannels = []
      #will add method for changing inport/outport in db

# todo implement DB connection
class Channel:
    def __init__(self, name, permissions, id, blockedUsers=[]):
        self.name = name
        self.blockedUsers = []
        self.users = []
        self.id = id
        self.permisions = permissions

	#used to create a new channel, init is used to fetch existing one from db
    @staticmethod
    def createNew(name, permissions):
        if name == 'General':
            id = '0000000000000000'
        else:
            id = CommonUtil.createID()
        ch = Channel(name, permissions, id)
        regex = re.match(r'([01]{3})', permissions)
        if regex:
           ch.permisions = permissions
        else:
            ch.permisions = '011'
        db.newChannel(ch)
        return ch



# ----------------------------------------------------------------------------------------------------------------------------------
# Server class and subclasses
# ----------------------------------------------------------------------------------------------------------------------------------

class Server:
    def __init__(self):
        self.Outbound = {}
        self.Inbound = CommonUtil.Queue()
        self.Error = CommonUtil.Queue()
        self.Channels = []
        self.Channels.append(Channel('General','011','0000000000000000'))
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

    def dequeue(self):
        while True:
            msg = self.Inbound.Pop()
            if msg:  # pop returns none if nothing is on que, not entering processing
                if msg.messageType == 'command':  # checking if message is a command
                    # for loop runs over every command type, only one matches, running inner if  once for processing
                    for command in CommonUtil.commands:
                        regex = re.match(CommonUtil.commands[command], msg.message)
                        print regex.group(0)
                        if regex:
                            if command == 'join':
                                ch = db.getChannel(regex.group(0))
                                if ch:
                                    error= db.addUser(msg.messageChannelId, msg.messageSenderId)  # returns none if successful
                                    if error:
                                        pass # send error

                            if command == 'create':
                                ch = db.getChannel(regex.group(0))
                                if ch:
                                    pass  # send user duplicate channel name error msg
                                else:
                                    c = Channel.createNew(regex.group(0), regex.group(1))
                                    error = db.newChannel(c)
                                    if error:
                                        pass # send error message
                                    else:
                                        db.addUser(c.id, msg.messageSenderId)

                            if command == 'set_alias':
                                if db.getUserAlias(regex.group(0)):
                                    pass # send error message
                                else:
                                    u = None #will add user initialization
                                    db.changeUser(msg.messageSenderId, u)

                            if command == 'block':
                                if db.userHasPermisions(msg.messageSenderId, msg.messageChannelId):
                                    if db.getUser(regex.group(0)):
                                        db.getChannel(msg.messageChannelId).blockUser(db.getUser(regex.group(0)))

                            if command == 'unblock':
                                if db.userHasPermisions(msg.messageSenderId, msg.messageChannelId):
                                    if db.getUser(regex.group(0)):
                                        db.UnblockUser(msg.messageChannelId, regex.group(0))

                            if command == 'delete':
                                if db.userHasPermisions(msg.messageSenderId, msg.messageChannelId):
                                    if db.deleteChannel(msg.messageChannelId):
                                        pass#send error(unable to delete)
                                else:
                                    pass#send permissions error

                            if command == 'chmod':
                                if db.userHasPermisions(db.getUser(msg.messageSenderId), db.getChannel(msg.messageChannelId)):
                                    if regex.group(0) == msg.messageChannelId:
                                        db.setChannelPermisions(msg.messageChannelId)
                                    elif db.IsMember(msg.messageChannelId, msg.messageChannelId):
                                        db.SetChannelPermisions(msg.messageChannelId, msg.messageChannelId, regex.group(1))
                                    else:
                                        pass  # send error msg

                        else:
                            pass  # send command not found error message

                else:
                    print(msg.message)
                    for u in self.users:
                        if u.id != msg.messageSenderId and u.currentchannel == msg.messageChannelId:
                            self.Outbound[u.inport].Push(msg)


if __name__ == '__main__':
    server = Server()
    threading._start_new_thread(server.dequeue, ())  # starts thread for handling outbound messages
	
    # setting up port for connecting to clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    server_socket.bind((host, port))
    server_socket.listen(10)
	
    #while loop for handling new connections
    while True:
        clientsocket, addr = server_socket.accept()
        print('Got a connection from %s' % str(addr))
        p1 = server.handler.port.pop()
        p2 = server.handler.port.pop()
        
        alias = clientsocket.recv(1024)
        user = db.getUserAlias(alias)
        
        if user:
            user = User(user[0], user[1], p1, p2)
            uID = user[2]
        else:
            uID=CommonUtil.createID()
            user = User(alias,uID,p1,p2)
            db.newUser(user)
        # sending the client the information on ports used
        k = str(uID) + '|' + str(p1)+'|'+str(p2)
        clientsocket.send(k.encode('utf8'))

        # starting threads to manage connection
        server.Outbound[p1] = CommonUtil.Queue()
        server.Outbound[p1].Push(welcome_message())
        server.users.append(User('', newuserid, p1, p2))
        threading._start_new_thread(CommonUtil.outbound_connection_handler, (p1, functools.partial(server.send, server),server.error,))
        time.sleep(0.05)
        threading._start_new_thread(CommonUtil.inbound_connection_handler, (p2, functools.partial(server.enqueue, server),server.error,))
        clientsocket.close()