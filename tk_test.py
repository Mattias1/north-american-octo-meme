from tkinter import *
from tkinter.ttk import *
from MattyControls import *


class Application(Frame):
    def say_hi(self):
        print("Hi there, everyone!")

    def createWidgets(self):
        #self.QUIT = Button(self)
        #self.QUIT["text"] = "QUIT"
        ## self.QUIT["fg"] = "red"
        #self.QUIT["command"] = self.quit
        #self.QUIT.pack({"side": "left"})

        self.btnQuit = Btn("Quit", self)
        self.btnQuit.command = self.quit

        self.btnHi = Btn("Hello", self)
        self.btnHi.command = self.say_hi

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()

