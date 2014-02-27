from tkinter import *
from tkinter.ttk import *
from threading import Thread
from time import sleep

from factory import Factory
import machines

class Application(Frame):
    running = False

    def __init__(self, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        self.create_widgets()
        self.refresh_rate = 1#20

    def create_widgets(self):
        """Create all the buttons and other widgets"""
        self.master.title("DVD Simulation")
        padding = {'padx': 5, 'pady': 5}
        self.pack(anchor=NW, fill=X, expand=1, **padding)

        # The frame for all the buttons
        control_frame = Frame(self, relief=RAISED, borderwidth=1)
        control_frame.pack(anchor=N)
        btn = Button(control_frame, text="New", command=self.new)
        btn.pack(anchor=NW, side=LEFT, **padding)
        btn = Button(control_frame, text="Play", command=self.play)
        btn.pack(anchor=NW, side=LEFT, **padding)
        btn = Button(control_frame, text="Pause", command=self.pause)
        btn.pack(anchor=NW, side=LEFT, **padding)
        btn = Button(control_frame, text="Step", command=self.step)
        btn.pack(anchor=NW, side=LEFT, **padding)
        btn = Button(control_frame, text="Stop", command=self.stop)
        btn.pack(anchor=NW, side=LEFT, **padding)
        btn = Button(control_frame, text="Exit", command=self.exit)
        btn.pack(anchor=NW, side=LEFT, **padding)

        # The machine stats
        stat_frame = Frame(self)
        stat_frame.pack(anchor=NW, fill=BOTH, expand=1)
        self.machinesA = Label(stat_frame, text='A')
        self.machinesA.pack(anchor=NW, side=LEFT, **padding)
        self.machinesB = Label(stat_frame, text='B')
        self.machinesB.pack(anchor=NW, side=LEFT, **padding)
        self.machinesC = Label(stat_frame, text='C')
        self.machinesC.pack(anchor=NW, side=LEFT, **padding)
        self.machinesD = Label(stat_frame, text='D')
        self.machinesD.pack(anchor=NW, side=LEFT, **padding)

        # The factory stats
        self.output = Label(text='Here comes the stats')
        self.output.pack(anchor=NW, side=LEFT, **padding)

    def new(self):
        self.stop()
        self.factory = Factory(10, 7)
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
            # Machine A-D
            mtypes = [machines.MachineA, machines.MachineB, machines.MachineC, machines.MachineD]
            mlabels = [self.machinesA, self.machinesB, self.machinesC, self.machinesD]
            for i in range(4):
                mtype = mtypes[i]
                messages = []
                for machine in self.factory.machines:
                    if mtype == machine.__class__:
                        text = [mtype.__name__ + ':']
                        for key, value in machine.stats.items():
                            text.append(key + ': ' + str(value))
                        messages.append('\n'.join(text))
                mlabels[i].config(text='\n\n'.join(messages))

            # Factory
            messages = ['STATS:']
            for key, value in self.factory.stats.items():
                messages.append(key + ': ' + str(value))
            self.write('\n'.join(messages))

            sleep(1 / self.refresh_rate)

    def write(self, message):
        self.output.config(text=message)


def main():
    """The main entrypoint for this application"""
    root = Tk()
    root.geometry("750x600")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    print('gui main')
    main()
