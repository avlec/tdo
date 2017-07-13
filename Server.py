import socket
import sys
import threading
import CommonUtil
import functools

def welcome_message():
    data = CommonUtil.Message.pack('0000000000000000', '0000000000000000','0000000000000000',"welcome to TDO communication services").encode('utf8')
    port = 0
    return CommonUtil.Message(data,port)

# currently a clusterfuck, todo and implement with db
class MessageGroup:
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
            self.id = CommonUtil.createID()
            self.name = name
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
                #send error

        def add_user(self, user):
            self.users.append(user)

    def __init__(self):
        self.size = 0
        self.client_list = []
        self.message_groups = []
        self.message_groups.append(self.Channel("general", None))

    def addClient(self, new):
        self.client_list.append(new)
        self.message_groups[0].add_user(new)


# ----------------------------------------------------------------------------------------------------------------------------------
# Server class and subclasses
# ----------------------------------------------------------------------------------------------------------------------------------

class Server:
    def __init__(self):
        self.Outbound = {}
        self.Inbound = CommonUtil.Queue()
        self.Error = CommonUtil.Queue()
        self.MessageGroupList = MessageGroup()
        self.handler = self.PortHandler()


    class PortHandler:
        def __init__(self):
            self.port = []
            for i in range(20000, 10000, -1):
                self.port.append(i)
    @staticmethod
    def send(server, p):
        msg = server.Outbound[p].Pop()
        if msg:
            return msg.packmessage()

    def enqueue(self, port, data):
        def validate(data):
            pass

        def enqueue(self, message):
            self.Inbound.Push(message)

        def dequeue(self):
            msg = self.Inbound.Pop()
            for key in self.Outbound:
                self.Outbound[key].Push(msg)

        validate(data)
        print (str(port)+":"+data.decode())
        msg = CommonUtil.Message(data, port)
        enqueue(self, msg)
        dequeue(self)#temp method, will move somewhere, do it independantly on a loop in thread





if __name__ == "__main__":
    server = Server()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    server_socket.bind((host, port))
    server_socket.listen(10)
    while True:
        clientsocket,addr = server_socket.accept()
        print("Got a connection from %s" % str(addr))
        p1 = server.handler.port.pop()
        p2 = server.handler.port.pop()
        # sending the client the information on ports used
        k =str(p1)+"|"+str(p2)
        clientsocket.send(k.encode('utf8'))

        # starting threads to manage connection
        server.Outbound[p1] = CommonUtil.Queue()
        server.Outbound[p1].Push(welcome_message())
        threading._start_new_thread(CommonUtil.outbound_connection_handler, (p1, functools.partial(server.send, server),))
        threading._start_new_thread(CommonUtil.inbound_connection_handler, (p2, functools.partial(server.enqueue, server),))

        clientsocket.close()