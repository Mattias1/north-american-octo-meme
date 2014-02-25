from queue import PriorityQueue
from machines import MachineA


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

    def __init__(self):
        self.machines = [MachineA(self)]
        PriorityQueue.__init__(self)

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

    def schedule(self, time, handler):
        assert time >= 0
        event = Event(self.cur_time + time, handler)
        self.put(event)
