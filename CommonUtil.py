import socket
import random

# ----------------------------------------------------------------------------------------------------------------------------------
# utility classes, Message, Queue, connection error
# ----------------------------------------------------------------------------------------------------------------------------------
# message class used to process messages
# format: message id|message sender id|message channel id|message
# ids are 10 digits, message is limited to 256 characters
# sample: 0000000000|0000000000|0000000000|Hello world

#alec redo to xml if you feel like it, but make function in to pack and unpack to this class
class Message:
    def __init__(self, data,port):
        inputList = data.decode().split('|')
        self.messageId = inputList[0]
        self.messageSenderId = inputList[1]
        self.messageChannelId = inputList[2]
        self.message = inputList[3]
        self.validate()

    # someone do this
    def validate(self):
        pass

    # pack class used to send a message in this format
    def pack(self,messageId,messageSenderId,messageChannelId,message):
        return messageId + '|' + messageSenderId + '|' + messageChannelId + '|'+ message

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
        self.expr = "connection error"
        self.msg = msg

# ----------------------------------------------------------------------------------------------------------------------------------
# end of utility classes
# ----------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------
# Utillity functions: connection handlers
# ----------------------------------------------------------------------------------------------------------------------------------


def outbound_connection_handler(port, handler):
    print("outbound port is :" + str(port) + "\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.bind((host, port))
    s.listen(2)
    serversocket,addr = s.accept()
    while True:
        msg = handler()
        serversocket.send(msg.encode('utf8'))
    serversocket.close()


def inbound_connection_handler(port, handler):
    print("inbound port is :" + str(port) + "\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = (host, port)
    s.connect(addr)
    while True:
        data = s.recv(1024)
        if not data:
            raise connection_error("invalid data")
        handler(port, data)
    s.close()

def createID():
    return str(random.randint(1000000000, 9999999999))