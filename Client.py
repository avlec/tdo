import threading
import socket
import sys
import CommonUtil
import random
import string
import time
import re
import Tkinter
import json
import GUI_Main
from messages.Message import Message as Message


# main class for client
class Client:
    def __init__(self):
        self.id = '0000000000000000'
        root2 = Tkinter.Tk()
        self.guiL = GUI_Main.login(root2)
        root2.mainloop()
        self.alias = self.guiL.username
        self.activeUsers = []
        self.activeChannels = []
        self.gui = None
        threading._start_new_thread(self.chat_client, ())

    # starting the gui for the chat
    def chat_client(self):
        root = Tkinter.Tk()
        self.gui = GUI_Main.GUI_MainPg(root)
        root.mainloop()


    # gets user input, handler function for outbound connection
    def get_input(self, p):
        while True:
            msg = None
            if self.gui:
                msg = self.gui.messageQueue.Pop()
            if msg:
                return Message(CommonUtil.createID(), self.id, None, msg).encode()


    # handler function for inbound connection
    def print_message(self, data):
        messages =[]
        msg = ''
        for m in data:
            if m != '}':
                msg += m
            else:
                msg+=(m)
                messages.append(msg)
                msg = ''
        print messages
        for msg in messages:
            msg = Message.decode(msg)
            if CommonUtil.command(msg.message, CommonUtil.serverCommands):
                for command in CommonUtil.serverCommands:
                    regex = re.match(CommonUtil.serverCommands[command], msg.message)
                    if regex:
                        if command == 'addUser':
                            self.activeUsers.append(regex.group(1))
                            self.gui.updateOnline(self.activeUsers)
                        if command == 'removeUser':
                            self.activeUsers.remove(regex.group(1))
                            self.gui.updateOnline(self.activeUsers)
                        if command == 'addChannel':
                            self.activeChannels.append(regex.group(1))
                            self.gui.updateRooms(self.activeChannels)
                        if command == 'removeChannel':
                            self.activeChannels.remove(regex.group(1))
                            self.gui.updateRooms(self.activeChannels)
                        if command == 'loginfailed':
                            pass

            else:
                #print(msg.senderAlias + ':' + msg.message)
                self.gui.updateChat(msg.senderAlias + ':' + msg.message + '\n', 'black', msg.messageId)


if __name__ == '__main__':
    C = Client()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    addr = (host, port)
    s.connect(addr)
    s.send(C.alias.encode('utf8'))
    connection_port = s.recv(1024)
    ports = connection_port.decode('utf8').split('|')
    C.id = ports.pop()
    p1 = ports.pop()
    p2 = ports.pop()

    print('my port is ' + p1 + '' and '' + p2)
    outbound = threading.Thread(target=CommonUtil.outbound_connection_handler, args=(int(p1), C.get_input),)
    inbound = threading.Thread(target=CommonUtil.inbound_connection_handler, args=(int(p2), C.print_message),)
    outbound.start()
    time.sleep(0.05)
    inbound.start()

    while True:
        pass
    sys.exit(0)
