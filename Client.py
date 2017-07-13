import threading
import socket
import sys
import CommonUtil

# format: message id|message sender id|message channel id|message
# ids are 10 digits, message is limited to 256 characters
# sample: 0000000000|0000000000|0000000000|Hello world


class Client:
    def __init__(self):
        self.id = None
        self.currentChannel = None

    def chat_client(self):
        pass

def get_input():
    msg = raw_input('alias:')
    return msg

def print_byte(port,data):
    print(data.decode())

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    addr = (host, port)
    s.connect(addr)
    connection_port = s.recv(1024)
    ports = connection_port.decode('utf8').split("|")
    p1 = ports.pop()
    p2 = ports.pop()
    print("my port is " + p1 + " and " + p2)

    threading._start_new_thread(CommonUtil.inbound_connection_handler, (int(p2),print_byte,))
    threading._start_new_thread(CommonUtil.outbound_connection_handler, (int(p1),get_input,))
    while True:
        pass
    sys.exit(0)