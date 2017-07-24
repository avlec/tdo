from tkinter import *
import tkinter.messagebox
# ******** the main page *************
class GUI_MainPg:

    def __init__(self,master):

        frame = Frame(master)
        frame.pack()
        master.bind('<Return>', self.enter)
        title = Label(frame, text="TDO")

        textField=Text(frame, width = 35, height = 13)
        roomName = Text(frame, width=25, height=5)
        send = Button(frame, text="Send", command=self.sendPressed)
        mainText = Entry(frame)
        room2Join = Entry(frame)
        roomJoin = Button(frame, text="Send", command=self.send2Pressed)

        online =Text(frame, width=25, height=5)


        title.grid(row=0, columnspan=7)
        textField.grid(row=1, columnspan=2, rowspan= 3)
        roomName.grid(row=1, column=3, columnspan=2)
        room2Join.grid(row=2,column=3, sticky= E)
        roomJoin.grid(row=2,column=4, sticky = W)
        mainText.grid(row=4, column=0, sticky = E)
        send.grid(row=4, column=1, sticky = W)
        online.grid(row =3, column =3, columnspan = 2)


        textField.config(state=DISABLED)
        roomName.config(state=DISABLED)

# -------- buttons/functions---------
    def sendPressed(self):
        print("send button pressed")

    def send2Pressed(self):
        print("room button pressed")

    def enter(self,event):
        print("enter key")

    def update (self, string):
        self.textField.config(state=NORMAL)
        self.textField.insert(END , string)
        self.textField.config(state=DISABLED)

# *********** the Login Page ***********
class login:
    def __init__(self, master):

        submit = Button(master, text="Login", command=self.loginButton)

        Title = Label(master, text="TDO")

        #img = PhotoImage(file='eggsml.png')
        #image = Label(master, image=img)

        message = Label(master, text="You're premier message delivery system.")

        field1 = Entry(master)



        Title.grid(row=0, columnspan=2)
        #image.grid(row=1, columnspan=2)
        message.grid(row=2, columnspan=2)
        field1.grid(row=3, column=0, sticky=E)
        submit.grid(row=3, column=1, sticky=W)

# ----- button functions -------
    def loginButton(self):
        print("login button pressed")

    def enter(self,event):
        print("enter button pressed")








root2 = Tk()
guiL = login(root2)
root2.mainloop()

root = Tk()
gui = GUI_MainPg(root)
root.mainloop()

