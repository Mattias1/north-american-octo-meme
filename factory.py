"""This module contains the factory class"""
from queue import PriorityQueue
from machines import MachineA, MachineB, MachineC, MachineD, BROKEN
from samples import samplesA, samplesB, samplesD
from buffers import Buffer, AssemblyLine
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
        return (self.time == obj.time and self.priority > obj.priority
                or self.time < obj.time)

    def __str__(self):
        return '{}, {}: {}.{}'.format(self.time, self.priority,
                                      self.handler.__self__.__class__.__name__,
                                      self.handler.__name__[0:20]
                                      )


class Factory(PriorityQueue):
    cur_time = 0
    stats = {}

    its_day = True

    EOS = False
    running = False
    do_one_step = False

    def __init__(self, repairmen_day, repairmen_night):
        PriorityQueue.__init__(self)
        self.machines = []

        samplesA.sort()
        samplesB.sort()
        samplesD.sort()

        bufferA12 = Buffer(self, 20)
        bufferA34 = Buffer(self, 20)
        machineA1 = MachineA(self, bufferA12)
        machineA2 = MachineA(self, bufferA12)
        machineA3 = MachineA(self, bufferA34)
        machineA4 = MachineA(self, bufferA34)
        bufferA12.providers = [machineA1, machineA2]
        bufferA34.providers = [machineA3, machineA4]

        bufferB1 = AssemblyLine(self, 20)  # Assembly line
        bufferB2 = AssemblyLine(self, 20)  # Assembly line
        machineB1 = MachineB(self, bufferB1)
        machineB2 = MachineB(self, bufferB2)
        machineB1.providers = [bufferA12, bufferA34]
        machineB2.providers = [bufferA12, bufferA34]
        bufferA12.receivers = [machineB1, machineB2]
        bufferA34.receivers = [machineB1, machineB2]
        bufferB1.providers = [machineB1]  # Assembly line
        bufferB2.providers = [machineB2]  # Assembly line

        bufferC1 = Buffer(self, 20)
        bufferC2 = Buffer(self, 20)
        machineC1 = MachineC(self, bufferC1)
        machineC2 = MachineC(self, bufferC2)
        machineC1.providers = [bufferB1]
        machineC2.providers = [bufferB2]
        bufferB1.receivers = [machineC1]  # Assembly line
        bufferB2.receivers = [machineC2]  # Assembly line
        bufferC1.providers = [machineC1]
        bufferC2.providers = [machineC2]

        machineD1 = MachineD(self)
        machineD2 = MachineD(self)
        machineD1.providers = [bufferC1, bufferC2]
        machineD2.providers = [bufferC1, bufferC2]
        bufferC1.receivers = [machineD1, machineD2]
        bufferC2.receivers = [machineD1, machineD2]

        self.machines = [machineA1, machineA2, machineA3, machineA4, machineB1,
                         machineB2, machineC1, machineC2, machineD1, machineD2]

        self.available_repairmen = repairmen_day
        self.repairman_day_night_difference = repairmen_day - repairmen_night

    def update_stats(self):
        # Update your own stats
        self.stats['- time'] = self.cur_time
        self.stats['- available repairmen'] = self.available_repairmen
        self.stats['- time of day'] = 'day' if self.its_day else 'night'
        temp_list = []
        temp_string = ''
        for _ in range(10):
            if not self.empty():
                temp_list.append(self.get())
        for evt in temp_list:
            self.put(evt)
            temp_string += '\n' + str(evt)
        self.stats['- queue items'] = '({}) {}'.format(self.qsize(), temp_string)

        # Update the stats of the machines
        for machine in self.machines:
            machine.update_stats()

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
            self.check_change_day_night()
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

    def check_change_day_night(self):
        # Assumptions: - At time 0 it is 6 am (start of the day). - A repairman finishes his job before he goes home.
        nr_half_days = self.cur_time // (12 * 3600)
        if (nr_half_days % 2 == 0) != self.its_day:
            self.its_day = not self.its_day
            if self.its_day:
                self.available_repairmen += self.repairman_day_night_difference
            else:
                # If this is negative, the repairman will finish the job, and go home afterwards
                self.available_repairmen -= self.repairman_day_night_difference

    def schedule(self, time, handler, priority=0):
        assert time >= 0
        event = Event(self.cur_time + time, handler, priority)
        self.put(event)

if __name__ == '__main__':
    import gui
    print('factory main')
    gui.main()
