from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
#from MattyControls import *


class Application(Frame):
    def say_hi(self):
        """Print Hi to the console"""
        print("Hi there, everyone!")

    def createWidgets(self):
        """Create all the buttons and other widgets"""
        self.master.title("Test")
        self.pack(fill=BOTH, expand=1)


        test = Button(self, text="test", command=self.quit)
        test.place(x=10, y=11)
        messagebox.showinfo("msg", test.winfo_width)
        self.quit()

        #self.btnHi = Btn(self)
        #self.btnHi.text = "Hello"
        #self.btnHi.command = self.say_hi
        #self.btnHi.locateInside(self, H_LEFT, V_TOP, 10)

        #self.btnQuit = Btn(self, text="Quit", command=self.quit)
        #self.btnQuit.locateFrom(self.btnHi, H_LEFT, V_COPY_TOP, 10)

        #self.btnTest = Btn(self, text="Test - quit", command=self.quit)
        #self.btnTest.locateFrom(self.btnHi, H_COPY_LEFT, V_BOTTOM, 10)

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
