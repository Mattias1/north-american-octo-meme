"""This module contains the factory class"""
from queue import PriorityQueue
from machines import MachineA, MachineB


class Event:
    def __init__(self, time, handler):
        self.time = time
        self.handler = handler

    def __call__(self):
        self.handler()

    def __lt__(self, obj):
        assert obj.__class__ == Event
        return self.time < obj.time


class Factory(PriorityQueue):
    cur_time = 0
    EOS = False

    def __init__(self, a, b, c, d, repairmen):
        PriorityQueue.__init__(self)
        self.machines = [MachineA(self), MachineB(self)]
        self.available_repairmen = repairmen

    def __str__(self):
        return ('time elapsed: {}\n'.format(self.cur_time) +
                '\n'.join([str(m) for m in self.machines]))

    def start(self):
        self.schedule(1000, self.stop)
        for machine in self.machines:
            machine.start_producing()

        while not self.empty() and not self.EOS:
            event = self.get()
            assert event.time >= self.cur_time
            self.cur_time = event.time
            event.handler()
        print(str(self))

    def stop(self):
        self.EOS = True

    def add_repairman(self):
        # Check if there is a machine broken right now, and do stuff with it
        if self.available_repairmen == 0:
            for machine in self.machines:
                if machine.status == BROKEN:
                    self.schedule(0, machine.start_repair)
                    return
        # If nothing has to be repaired right away, just let the poor guy drink his coffee
        self.available_repairmen += 1

    def schedule(self, time, handler):
        assert time >= 0
        event = Event(self.cur_time + time, handler)
        self.put(event)
