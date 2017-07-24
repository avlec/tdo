import threading
import socket
import sys
import CommonUtil
import random
import string
import time
import re
# format: message id|message sender id|sender alias|message channel id|message
# ids are 16 digits, message is limited to 256 characters
# sample: 0000000000000000|0000000000000000|server|0000000000000000|Hello world
from messages.Message import Message as Message


class Client:
    def __init__(self):
        self.id = '0000000000000000'
        self.currentChannel = '0000000000000000'
        self.alias = 'bob' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

    def chat_client(self):
        pass

    def command(self,str):
        #regex objects for each command
        for command in CommonUtil.commands:
            if re.match(CommonUtil.commands[command], str):
                print('command sent')
                return True
        return False

    def get_input(self, p):
        msg = raw_input()

        if self.command(msg):
            return Message(CommonUtil.createID(), self.id, self.alias, self.currentChannel, msg, 'command').encode()
        elif re.match(r'\/.+', msg):
            print('commands info:')#add a print out of all commands info
        else:
            return Message(CommonUtil.createID(), self.id, self.alias, self.currentChannel, msg, 'message').encode()


def print_message(data):
    msg = Message.decode(data)
    print(msg.senderAlias + ':' + msg.message)

if __name__ == '__main__':
    C = Client()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    addr = (host, port)
    s.connect(addr)
    connection_port = s.recv(1024)
    ports = connection_port.decode('utf8').split('|')
    p1 = ports.pop()
    p2 = ports.pop()
    C.id = ports.pop()
    print('my port is ' + p1 + '' and '' + p2)
    threading._start_new_thread(CommonUtil.outbound_connection_handler, (int(p1), C.get_input,))
    time.sleep(0.05)
    threading._start_new_thread(CommonUtil.inbound_connection_handler, (int(p2), print_message,))


    while True:
        pass
    sys.exit(0)
