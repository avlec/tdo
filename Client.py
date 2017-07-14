import threading
import socket
import sys
import CommonUtil
import random
import string
import time
# format: message id|message sender id|sender alias|message channel id|message
# ids are 16 digits, message is limited to 256 characters
# sample: 0000000000000000|0000000000000000|server|0000000000000000|Hello world


class Client:
    def __init__(self):
        self.id = '0000000000000000'
        self.currentChannel = '0000000000000000'
        self.alias = 'bob' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

    def chat_client(self):
        pass

    def get_input(self, p):
        msg = raw_input()
        return CommonUtil.Message.pack(CommonUtil.createID(), self.id, self.alias, self.currentChannel, msg)


def print_byte(data):
    msg = CommonUtil.Message(data)
    print msg.senderAlias + ':' + msg.message

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
    threading._start_new_thread(CommonUtil.inbound_connection_handler, (int(p2),print_byte,))


    while True:
        pass
    sys.exit(0)
