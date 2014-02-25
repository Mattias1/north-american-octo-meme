from tkinter import *
from tkinter.ttk import *


class Application(Frame):
    @staticmethod
    def say_hi():
        """Print Hi to the console"""
        print("Hi there, everyone!")

    def create_widgets(self):
        """Create all the buttons and other widgets"""
        self.master.title("Test")
        padding = {'padx': 5, 'pady': 5}

        self.pack(fill=BOTH, expand=1, **padding)

        self.bhi = Button(self, text="Hello", command=self.say_hi)
        self.bhi.pack(anchor=NW, side=LEFT, **padding)

        self.bquit = Button(self, text="Quit", command=self.quit)
        self.bquit.pack(anchor=NW, side=LEFT, **padding)

        self.btest = Button(self, text="Test")
        self.btest.pack(anchor=NE, **padding)

    def __init__(self, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        self.create_widgets()


def main():
    """The main entrypoint for this application"""
    root = Tk()
    root.geometry("350x200")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
