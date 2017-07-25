from tkinter import *
import tkinter.messagebox
# ******** the main page *************
class GUI_MainPg:

    def __init__(self,master):
        # the main frame
        self.frame = Frame(master)
        self.frame.pack()
        #title
        self.title = Label(self.frame, text="TDO")
        # the field with messages deploying
        self.textField=Text(self.frame, width = 35, height = 13)
        #the field with rooms to join visible
        self.roomName = Text(self.frame, width=25, height=5)
        # send button
        self.send = Button(self.frame, text="Send", command=self.sendPressed)
        # the main chat bar
        self.mainText = Entry(self.frame)
        self.mainText.bind('<Return>', self.enter)
        #the room to join text bar
        self.room2Join = Entry(self.frame)
        self.room2Join.bind('<Return>', self.altEnter)
        #button for join room
        self.roomJoin = Button(self.frame, text="Send", command=self.send2Pressed)
        #field for users online
        self.online =Text(self.frame, width=25, height=5)



        # the placement of objects in the grid
        self.title.grid(row=0, columnspan=7)
        self.textField.grid(row=1, columnspan=2, rowspan= 3)
        self.roomName.grid(row=1, column=3, columnspan=2)
        self.room2Join.grid(row=2,column=3, sticky= E)
        self.roomJoin.grid(row=2,column=4, sticky = W)
        self.mainText.grid(row=4, column=0, sticky = E)
        self.send.grid(row=4, column=1, sticky = W)
        self.online.grid(row =3, column =3, columnspan = 2)


        self.textField.config(state=DISABLED)
        self.roomName.config(state=DISABLED)
        self.online.config(state=DISABLED)

# -------- buttons/functions---------
    def sendPressed(self):
        print(self.mainText.get())

    def send2Pressed(self):
        print(self.roomName.get())

    def enter(self,event):
        print(self.mainText.get())
    # the function for the room join enter key being pushed.
    def altEnter(self, event):
        print(self.roomName.get())

    def updateChat (self, string):
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
        print(login.get())

    def enter(self,event):
        print()








root2 = Tk()
guiL = login(root2)
root2.mainloop()

root = Tk()
gui = GUI_MainPg(root)
root.mainloop()


