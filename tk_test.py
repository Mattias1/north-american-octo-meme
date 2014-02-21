from tkinter import *
from tkinter.ttk import *
#from MattyControls import *


class Application(Frame):
    def say_hi(self):
        print("Hi there, everyone!")

    def createWidgets(self):
        self.master.title("Test")
        self.pack(fill=BOTH)

        self.btnHi = Button(self, text="Hello", command=self.say_hi)
        self.btnHi.pack(side=LEFT, padx=10, pady=10)
        #self.btnHi.place(x=10, y=10)

        self.btnQuit = Button(self, text="Quit", command=self.quit)
        self.btnQuit.pack(side=LEFT, padx=0, pady=10)
        #self.btnQuit.place(x=50, y=10)

        self.btnTest = Button(self, text="Test", command=self.quit)
        self.btnTest.pack(side=TOP, padx=0, pady=10)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()


root = Tk()
root.geometry("350x200")
app = Application(master=root)
app.mainloop()

