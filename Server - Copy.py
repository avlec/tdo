import Connector
import sys
import threading

# ----------------------------------------------------------------------------------------------------------------------------------
# utility classes, Message, Queue
# ----------------------------------------------------------------------------------------------------------------------------------
# message class used to process messages
# format: message id|message sender id|message channel id|message
# ids are 10 digits, message is limited to 256 characters
# sample: 0000000000|0000000000|0000000000|Hello world


class Message:
    def __init__(self, data, ip):
        inputList = data.decode().split('|')
        self.messageId = inputList[0]
        self.messageSenderId = inputList[1]
        self.messageChannelId = inputList[2]
        self.message = inputList[3]
        self.clientIP = ip
        self.validate()

    # someone do this
    def validate(self):
        pass


# Queue class used for storing messages during processing.
class Queue:
    def __init__(self):
        self.messages = []

    def Pop(self):
        if len(self.messages) > 0:
            return self.messages.pop(0)

    def Push(self, message):
        self.messages.append(message)

# ----------------------------------------------------------------------------------------------------------------------------------
# end of utility classes
# ----------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------
# database interface and data object classes(every data item has a class)
# ----------------------------------------------------------------------------------------------------------------------------------


# alec do this shit
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
            self.id = Connector.createID()
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

# alec do this shit
class DataBaseInterface:
    def __init__(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------------------
# Server class and subclasses
# ----------------------------------------------------------------------------------------------------------------------------------

class Server:
    def __init__(self):
        self.Outbound = Queue()
        self.Inbound = Queue()
        self.Error = Queue()
        self.MessageGroupList = MessageGroup()
        self.Main = Connector.Connection()
        threading._start_new_thread(self.proccessor(), (self,))

    def proccessor(self):
        while True:
            message = self.Inbound.Pop()
            if message:
                print(message)



    def enqueue(self, data):
        def validate(data):
            pass

        def enqueue(message):
            self.Inbound.Push(message)

        validate(data)
        msg = Message(data, 192.168)
        enqueue(msg)




# thread for each client
def ClientInboundThread(client):
        # Sending message to connected client
        # SERVER.Main.s.send(bytes('Welcome to Thine Digital Ostrich', encoding='utf8'))
        while True:
            # Receiving from client
            data = client.recv(1024)
            # reply = 'OK...' + data
            if not data:
                break
            print ("message recived")
            SERVER.enqueue(data)
            # add timeout in 10 mins?
        client.close()


def ClientOutboundThread():
    pass

if __name__ == "__main__":
    SERVER=Server()
    # add try except block, catch socket.error
    SERVER.Main.s.bind(SERVER.Main.address)
    SERVER.Main.s.listen(10)
    #main thread
    while 1:
        client, addr =  SERVER.Main.s.accept()
        threading._start_new_thread(ClientInboundThread, (client,))
    SERVER.Main.s.close()



