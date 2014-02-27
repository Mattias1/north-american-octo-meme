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
        self.refresh_rate = 20

    def create_widgets(self):
        """Create all the buttons and other widgets"""
        self.master.title("DVD Simulation")
        padding = {'padx': 5, 'pady': 5}

        self.pack(fill=BOTH, expand=1, **padding)

        btn = Button(self, text="New", command=self.new)
        btn.pack(anchor=NW, side=LEFT, **padding)

        btn = Button(self, text="Play", command=self.play)
        btn.pack(anchor=NW, side=LEFT, **padding)

        btn = Button(self, text="Pause", command=self.pause)
        btn.pack(anchor=NW, side=LEFT, **padding)

        btn = Button(self, text="Step", command=self.step)
        btn.pack(anchor=NW, side=LEFT, **padding)

        btn = Button(self, text="Stop", command=self.stop)
        btn.pack(anchor=NW, side=LEFT, **padding)

        btn = Button(self, text="Exit", command=self.exit)
        btn.pack(anchor=NW, side=LEFT, **padding)

        self.output = Label(text='Here comes the stats')
        self.output.pack(anchor=NW, side=LEFT, **padding)

    def new(self):
        self.stop()
        self.factory = Factory(1, 1, 1, 1, 10, 7)
        self.running = True
        sim_thread = Thread(target=self.factory.start)
        stats_thread = Thread(target=self.print_stats)
        sim_thread.start()
        stats_thread.start()

    def play(self):
        if self.running:
            self.factory.running = True

    def pause(self):
        if self.running:
            self.factory.running = False

    def step(self):
        if self.running:
            self.factory.step()

    def stop(self):
        if self.running:
            self.running = False
            self.factory.stop()

    def exit(self):
        self.stop()
        self.quit()

    def print_stats(self):
        while self.running:
            messages = ['STATS:']
            for key, value in self.factory.stats.items():
                messages.append(str(key) + ': ' + str(value))
            self.write('\n'.join(messages))
            sleep(1 / self.refresh_rate)

    def write(self, message):
        #print(message)
        self.output.config(text=message)



def main():
    """The main entrypoint for this application"""
    root = Tk()
    root.geometry("600x400")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    print('gui main')
    main()
