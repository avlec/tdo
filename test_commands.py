import random
import string
import threading
import socket
import sys
import CommonUtil
import time
from messages.Message import Message as Message


def getInput(m):
    while True:
        m = queue.Pop()
        if m:
            print ('\n'+ m.encode())
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
    print 'eeeeeeeeeeeeeee'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    addr = (host, port)
    s.connect(addr)
    alias = 'test'+CommonUtil.createID()
    print ('printing alias ' + alias)
    s.send(alias.encode('utf8'))
    connection_port = s.recv(1024)
    ports = connection_port.decode('utf8').split('|')
    id = ports.pop()
    p1 = ports.pop()
    p2 = ports.pop()

    print('my port is ' + p1 + '' and '' + p2)
    event = threading.Event()
    event.is_set = False
    outbound = threading.Thread(target=CommonUtil.outbound_connection_handler, args=(int(p1), event, getInput),)
    inbound = threading.Thread(target=CommonUtil.inbound_connection_handler, args=(int(p2), event, printMsg),)
    outbound.daemon = True
    inbound.daemon = True
    outbound.start()
    time.sleep(0.05)
    inbound.start()
    return (id, alias)


def test_basic_message():
    id = setup(queue)
    #insert any messages here, put delay inbetween messages if order matters
    m = Message('0000000000000000', id[0], id[1], 'Hello'.join(random.choice(string.ascii_uppercase + string.digits)))
    i = 0
    #change the last delay if you want test to run longer
    while i<50:
        queue.Push(m)
        time.sleep(1)
        i+=1
    sys.exit(0)
queue = CommonUtil.Queue()
test_basic_message()