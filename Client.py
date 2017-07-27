import threading
import socket
import sys
import CommonUtil
import random
import string
import time
import re
import Tkinter
import functools
import GUI_Main
from messages.Message import Message as Message

#main class for client
class Client:
    def __init__(self):
        self.id = '0000000000000000'
        self.currentChannel = '0000000000000000'
        #self.alias = 'bob' + ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        root2 = Tkinter.Tk()
        self.guiL = GUI_Main.login(root2)
		
		#starting log in screeen gui
        root2.mainloop()
        self.alias = self.guiL.username
        print('alec is a cunt')
        self.gui = None
        threading._start_new_thread(self.chat_client,())
        

	#starting the gui for the chat
    def chat_client(self):
        root = Tkinter.Tk()
        self.gui = GUI_Main.GUI_MainPg(root)
	root.protocol('WM_DELETE_WINDOW', on_closing)
        root.mainloop()
		
	#checks if comman is valid whe / is used
    def command(self,str):
        #regex objects for each command
        for command in CommonUtil.commands:
            if re.match(CommonUtil.commands[command], str):
                print('command sent')
                return True
        return False
    #gets user input, handler function for outbound connection
    def get_input(self, p):
        while True:
            msg = None
            if self.gui:
                msg = self.gui.messageQueue.Pop()
            if msg:
                if self.command(msg):
                    return Message(CommonUtil.createID(), self.id, self.alias, self.currentChannel, msg, 'command').encode()
                elif re.match(r'\/.+', msg):
                    print('commands info:')#add a print out of all commands info
                else:
                    return Message(CommonUtil.createID(), self.id, self.alias, self.currentChannel, msg, 'message').encode()
                
    #error function for inbound and outbound connections
    @staticmethod
    def error(port):
        errMessage = Message('0000000000000000', '0000000000000000', 'server', '0000000000000000', 'connection to server lost, shuting down','message').encode()
        #print(errMessage)
        C.print_message(errMessage)
        sys.exit(0)
	#handler function for inbound connection
    def print_message(self,data):
        msg = Message.decode(data)
        #print(msg.senderAlias + ':' + msg.message)
        self.gui.updateChat(msg.senderAlias + ':' + msg.message+'\n','black',msg.messageId)
        

if __name__ == '__main__':
    C = Client()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    addr = (host, port)
    s.connect(addr)
    s.send(C.username.encode('utf8'))
    connection_port = s.recv(1024)
    ports = connection_port.decode('utf8').split('|')
    p1 = ports.pop()
    p2 = ports.pop()
    C.id = ports.pop()
    print('my port is ' + p1 + '' and '' + p2)
    threading._start_new_thread(CommonUtil.outbound_connection_handler, (int(p1), C.get_input,C.error,))
    time.sleep(0.05)
    threading._start_new_thread(CommonUtil.inbound_connection_handler, (int(p2), C.print_message,C.error,))

    while True:
        pass
    sys.exit(0)
