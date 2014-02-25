from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *


class Application(Frame):
    def say_hi(self):
        """Print Hi to the console"""
        print("Hi there, everyone!")

    def createWidgets(self):
        """Create all the buttons and other widgets"""
        self.master.title("Test")
        self.pack(fill=BOTH, expand=1, padx=5, pady=5)

        self.btnHi = Button(self, text = "Hello", command = self.say_hi)
        self.btnHi.pack(anchor=NW, padx=5, pady=5)

        self.btnQuit = Button(self, text="Quit", command=self.quit)
        self.btnQuit.pack(anchor=NW, side=LEFT, padx=5, pady=5)

        self.btnTest = Button(self, text="Test - quit", command=self.quit)
        self.btnTest.pack(anchor=NW, padx=5, pady=5)

    def __init__(self, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        self.createWidgets()


def main():
    """The main entrypoint for this application"""
    root = Tk()
    root.geometry("350x200")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
