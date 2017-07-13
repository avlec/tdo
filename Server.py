import socket
import sys
import threading
import CommonUtil


# ----------------------------------------------------------------------------------------------------------------------------------
# database interface and data object classes(every data item has a class)
# ----------------------------------------------------------------------------------------------------------------------------------
class PortHandler:
    def __init__(self):
        self.port = []
        for i in range(20000, 10000, -1):
            self.port.append(i)


def print_message(port,data):
    print (str(port)+":"+data.decode())
def welcome_message():
    return ""

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
        self.Outbound = CommonUtil.Queue()
        self.Inbound = CommonUtil.Queue()
        self.Error = CommonUtil.Queue()
        self.MessageGroupList = MessageGroup()
        self.Main = CommonUtil.Connection()
        threading._start_new_thread(self.proccessor(), (self,))


    def enqueue(self, data):
        def validate(data):
            pass

        def enqueue(message):
            self.Inbound.Push(message)

        validate(data)
        msg = CommonUtil.Message(data)
        enqueue(msg)





if __name__ == "__main__":
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
        clientsocket.send(k.encode('utf8'))

        # starting threads to manage connection

        threading._start_new_thread(CommonUtil.outbound_connection_handler, (p1,welcome_message,))
        threading._start_new_thread(CommonUtil.inbound_connection_handler, (p2,print_message,))

        clientsocket.close()