"""This module contains the factory class"""
from queue import PriorityQueue
from machines import MachineA, MachineB, MachineC, MachineD, BROKEN, BORED
from time import sleep


class Event:
    def __init__(self, time, handler, priority):
        self.time = time
        self.priority = priority
        self.handler = handler

    def __call__(self):
        self.handler()

    def __lt__(self, obj):
        assert obj.__class__ == Event
        return (self.time == obj.time and self.priority > obj.priority) or self.time < obj.time

    def __str__(self):
        return '{}, {}: {}.{}'.format(self.time, self.priority,
                                      self.handler.__self__.__class__.__name__,
                                      self.handler.__name__[0:20]
                                     )


class Factory(PriorityQueue):
    cur_time = 0
    stats = {}

    EOS = False
    running = False
    do_one_step = False

    def __init__(self, a, b, c, d, repairmen_day, repairmen_night):
        PriorityQueue.__init__(self)
        self.machines = []
        for _ in range(a):
            self.machines.append(MachineA(self))
        for _ in range(b):
            self.machines.append(MachineB(self))
        for _ in range(c):
            self.machines.append(MachineC(self))
        for _ in range(d):
            self.machines.append(MachineD(self))
        self.available_repairmen = repairmen_day
        self.repairman_day_night_difference = repairmen_day - repairmen_night

    def __str__(self):
        return ('time elapsed: {}\n\n'.format(self.cur_time) +
                '\n'.join([str(m) for m in self.machines]) +
                '\nqueue length: ' + str(len(self)))

    def update_stats(self):
        self.stats['- time'] = self.cur_time
        # self.stats['- machines'] = '\n' + '\n'.join([str(m) for m in self.machines])
        temp_list = []
        temp_string = ''
        for _ in range(10):
            if not self.empty():
                temp_list.append(self.get())
        for evt in temp_list:
            self.put(evt)
            temp_string += '\n' + str(evt)
        self.stats['- queue items'] = '({}) {}'.format(self.qsize(), temp_string)

    def start(self):
        for machine in self.machines:
            if machine.__class__ == MachineA:
                self.schedule(0, machine.start_producing)
        self.update_stats()

        while not self.empty() and not self.EOS:
            # Manage sleeping
            if not self.running and not self.do_one_step:
                sleep(0.2)
                continue
            if self.do_one_step:
                self.do_one_step = not self.do_one_step

            # Manage events
            event = self.get()
            assert event.time >= self.cur_time
            self.cur_time = event.time
            event.handler()

            # Statistics
            self.update_stats()

    def play(self):
        self.running = True

    def pause(self):
        self.running = False

    def step(self):
        self.do_one_step = True

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

    def schedule(self, time, handler, priority=0):
        assert time >= 0
        event = Event(self.cur_time + time, handler, priority)
        self.put(event)

    def next_idle_machine(self, class_type):
        for machine in self.machines:
            if machine.__class__ == class_type and machine.status == BORED:
                return machine
        return None


if __name__ == '__main__':
    import gui
    print('factory main')
    gui.main()
