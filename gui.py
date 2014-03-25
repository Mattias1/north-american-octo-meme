from tkinter import *
from tkinter.ttk import *
from threading import Thread
from time import sleep
import random

from factory import Factory
import machines


class Application(Frame):
    running = False

    def __init__(self, master=None):
        """The constructor"""
        Frame.__init__(self, master)
        self.create_widgets()
        self.refresh_rate = 5

    def create_widgets(self):
        """Create all the buttons and other widgets"""
        self.master.title("DVD Simulation")
        padding = {'padx': 5, 'pady': 5}
        self.pack(anchor=NW, fill=X, expand=1, **padding)

        # The frame for all the buttons, and the buttons themselves
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

        self.seed_entry = Entry(control_frame)
        self.seed_entry.pack(anchor=NW, side=LEFT, **padding)
        self.seed_label = Label(control_frame, font=("Arial", 10))
        self.seed_label.pack(anchor=NW, side=LEFT, **padding)

        # The frame for the machine stats (and now also for the factory stats)
        stat_frame = Frame(self)
        stat_frame.pack(anchor=NW, fill=BOTH, expand=1)

        # The factory stats
        self.output = Label(stat_frame, text=self.facstr(), font=("Arial", 10))
        self.output.pack(anchor=NW, side=LEFT, **padding)

        # The machine stats
        self.machinesA = Label(stat_frame, text='Machine statistics:     A')
        self.machinesA.pack(anchor=NW, side=LEFT, **padding)
        self.machinesB = Label(stat_frame, text='B')
        self.machinesB.pack(anchor=NW, side=LEFT, **padding)
        self.machinesC = Label(stat_frame, text='C')
        self.machinesC.pack(anchor=NW, side=LEFT, **padding)
        self.machinesD = Label(stat_frame, text='D')
        self.machinesD.pack(anchor=NW, side=LEFT, **padding)

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value
        self.seed_label.config(font=("Arial", 10), text='current seed: ' + str(value))

    def new(self):
        self.stop()
        # If necessary, we can phone an extra repair guy, so we can just pick 11,8.
        # In practise this doesnt matter, as we are never short of repair guys.
        self.seed = self.seed_entry.get() or random.random()
        self.factory = Factory(11, 8, self.seed, 1000)
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
                        for key, value in sorted(machine.stats.items()):
                            text.append(' {}: {}'.format(key, value))
                        messages.append('\n'.join(text))
                mlabels[i].config(font=("Arial", 10), text='\n\n'.join(messages))

            # Factory
            messages = [self.facstr()]
            for key, value in sorted(self.factory.stats.items()):
                if key[0] == 'Q':
                    messages.append('')
                    messages.append('{}: {}'.format(key, value))
                else:
                    messages.append(' {}: {}'.format(key, value))
            self.write('\n'.join(messages))

            sleep(1 / self.refresh_rate)

    def write(self, message):
        self.output.config(font=("Arial", 10), text=message)

    @staticmethod
    def facstr():
        return 'Factory statistics:' + ''.join([' ' for _ in range(60)])


def main():
    """The main entrypoint for this application"""
    root = Tk()
    root.geometry("1260x685+10+0")
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    print('gui main')
    main()
