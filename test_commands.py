import threading
import socket
import sys
import CommonUtil
import string
import GUI_Main
import Client
import time
from messages.Message import Message as Message


def getInput(m):
    while True:
        m = queue.Pop()
        if m:
            return m.encode()

def printMsg(data):
    messages =[]
    msg = ''
    for m in data:
        if m != '}':
            msg += m
        else:
            msg+=(m)
            messages.append(msg)
            msg = ''
    for m in messages:
        msg = Message.decode(m)
        print(msg.senderAlias + ':' + msg.message)

def setup(queue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    addr = (host, port)
    s.connect(addr)
    s.send('test'.encode('utf8'))
    connection_port = s.recv(1024)
    ports = connection_port.decode('utf8').split('|')
    id = ports.pop()
    p1 = ports.pop()
    p2 = ports.pop()

    print('my port is ' + p1 + '' and '' + p2)
    outbound = threading.Thread(target=CommonUtil.outbound_connection_handler, args=(int(p1), getInput),)
    inbound = threading.Thread(target=CommonUtil.inbound_connection_handler, args=(int(p2), printMsg),)
    outbound.start()
    time.sleep(0.05)
    inbound.start()



queue = CommonUtil.Queue()
setup(queue)
#insert any messages here, put delay inbetween messages if order matters
m = Message('0000000000000000', '0000000000000000', 'server', 'Hello')
queue.Push(m)


#change the last delay if you want test to run longer
time.sleep(5)
sys.exit(0)