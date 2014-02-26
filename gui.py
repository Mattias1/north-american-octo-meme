from tkinter import *
from tkinter.ttk import *
from threading import Thread
from time import sleep

from factory import Factory

class Application(Frame):
    running = False

    def __init__(self, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        self.create_widgets()
        self.refresh_rate = 50

    def create_widgets(self):
        """Create all the buttons and other widgets"""
        self.master.title("DVD Simulation")
        padding = {'padx': 5, 'pady': 5}

        self.pack(fill=BOTH, expand=1, **padding)

        self.bhi = Button(self, text="Start", command=self.start)
        self.bhi.pack(anchor=NW, side=LEFT, **padding)

        self.bhi = Button(self, text="Stop", command=self.stop)
        self.bhi.pack(anchor=NW, side=LEFT, **padding)

        self.bquit = Button(self, text="Quit", command=self.exit)
        self.bquit.pack(anchor=NW, side=LEFT, **padding)

        self.output = Label(text='Here comes the stats')
        self.output.pack(side=LEFT, **padding)

    def start(self):
        if not self.running:
            self.factory = Factory(1, 0, 0, 0, 10)
            sim_thread = Thread(target=self.factory.start)
            stats_thread = Thread(target=self.print_stats)
            self.running = True
            sim_thread.start()
            stats_thread.start()

    def exit(self):
        self.stop()
        self.quit()

    def stop(self):
        if self.running:
            self.running = False
            self.factory.EOS = True

    def print_stats(self):
        while self.running:
            messages = ['STATS:']
            for key, value in self.factory.stats.items():
                messages.append(str(key) + ': ' + str(value))
            sleep(1 / self.refresh_rate)
            self.write('\n'.join(messages))

    def write(self, message):
        #print(message)
        self.output.config(text=message)



def main():
    """The main entrypoint for this application"""
    root = Tk()
    root.geometry("350x200")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
