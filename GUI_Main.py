from Tkinter import *
import CommonUtil


# ******** the main page *************
class GUI_MainPg:
    def __init__(self, master):
        self.root = master
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.messageQueue = CommonUtil.Queue()
        # the main frame
        self.frame = Frame(master)
        self.frame.pack()
        # title
        self.title = Label(self.frame, text="TDO")
        # the field with messages deploying
        self.textField = Text(self.frame, width=48, height=13)
        # the field with rooms to join visible
        self.roomName = Text(self.frame, width=25, height=6)
        # send button
        self.send = Button(self.frame, text="Send", command=self.sendPressed)
        # the main chat bar
        self.mainText = Entry(self.frame)
        self.mainText.bind('<Return>', self.enter)
        # the room to join text bar
        # button for join room
        # field for users online
        self.online = Text(self.frame, width=25, height=6)

        self.sp = Label(self.frame, text="     ")

        # the placement of objects in the grid
        self.title.grid(row=0, columnspan=7)
        self.textField.grid(row=1, columnspan=2, rowspan=3)
        self.roomName.grid(row=1, column=5, columnspan=2)
        self.sp.grid(column=4, row=2)

        # self.room2Join.grid(row=2,column=3, sticky= E)
        # self.roomJoin.grid(row=2,column=4, sticky = W)
        self.mainText.grid(row=4, column=0, sticky=E)
        self.send.grid(row=4, column=1, sticky=W)
        self.online.grid(row=3, column=5, columnspan=2)

        self.textField.config(state=DISABLED)
        self.roomName.config(state=DISABLED)
        self.online.config(state=DISABLED)

    # -------- buttons/functions---------
    def sendPressed(self):
        self.updateChat(self.mainText.get() + '\n','blue',CommonUtil.createID())
        self.messageQueue.Push(self.mainText.get())
        self.mainText.delete(0, END)

    def enter(self, event):
        self.updateChat(self.mainText.get() + '\n','blue',CommonUtil.createID())
        self.messageQueue.Push(self.mainText.get())
        self.mainText.delete(0, END)
        # the function for the room join enter key being pushed.
        # def altEnter(self, event):
        # print(self.roomName.get())

    def updateChat(self, string , color, msgID):
        self.textField.config(state=NORMAL)
        self.textField.insert(END, string, msgID)
        self.textField.tag_configure(msgID, foreground=color)
        self.textField.config(state=DISABLED)

    def updateRooms(self, string):
        self.roomName.config(state=NORMAL)      
        self.roomName.delete(0, END)
        for line in string:
            self.roomName.insert(END, line)
        self.roomName.config(state=DISABLED)

    def updateOnline(self, string):
        self.online.config(state=NORMAL)
        self.online.delete(0, END)
        for line in string:
            self.online.insert(END, line)
        self.online.config(state=DISABLED)
    def on_closing(self):
        self.root.destroy()
        sys.exit(0)

# *********** the Login Page ***********
class login:
    def __init__(self, master):
        self.master = master
        self.submit = Button(self.master, text="Login", command=self.loginButton)
        self.username = None
        self.Title = Label(self.master, text="TDO")

        # img = PhotoImage(file='eggsml.png')
        # image = Label(master, image=img)

        self.message = Label(self.master, text="You're premier message delivery system.")

        self.field1 = Entry(self.master)
        self.field1.bind('<Return>', self.enter)

        self.Title.grid(row=0, columnspan=2)
        # image.grid(row=1, columnspan=2)
        self.message.grid(row=2, columnspan=2)
        self.field1.grid(row=3, column=0, sticky=E)
        self.submit.grid(row=3, column=1, sticky=W)

    # ----- button functions -------
    def loginButton(self):
        self.username=self.field1.get()
        self.master.destroy()

    def enter(self, event):
        self.username=self.field1.get()
        self.master.destroy()

    def on_closing(self):
        self.root.destroy()
