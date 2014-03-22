"""This module contains the classes for buffers."""
from machines import BORED
from collections import deque


class Buffer:
    def __init__(self, factory, size):
        self.factory = factory
        assert size > 0
        self.size = size
        self.storage = []
        self.providers = []
        self.receivers = []

    def enough_room(self, amount=1):
        return len(self.storage) + amount <= self.size

    def add_product(self, batch):
        if len(self.storage) + len(batch) <= self.size:
            self.storage.extend(batch)
            # Since we have a non empty storage, try to activate all receivers
            for machine in self.receivers:
                if machine.status == BORED:
                    self.factory.schedule(0, machine.start_producing)
        else:
            raise Exception('Buffer overflow.')

    def remove_product(self, amount=1):
        if len(self.storage) >= amount:
            # Since we have a non full storage, try to activate all providers
            for machine in self.providers:
                if machine.status == BORED:
                    machine.start_producing()
            return [self.storage.pop() for _ in range(amount)]
        else:
            raise Exception('Buffer underflow.')


class AssemblyLine(Buffer):
    halted = False

    def __init__(self, factory, size):
        super().__init__(factory, size)
        self.line = deque()
        self.next_batch = []

    def add_product(self, batch):
        if self.enough_room():
            self.put_on_line(batch)
        else:
            raise Exception('Assembly line overflow.')

    def put_on_line(self, batch):
        """Puts product on assembly line."""
        total_queue_time = sum([time for time, batch in self.line])
        assert total_queue_time <= 5
        self.line.appendleft((5 - total_queue_time, batch))
        self.halted = False

        if len(self.line) == 1:
            self.factory.schedule(5, self.put_in_crate)

    def put_in_crate(self):
        """Puts product in crate after assembly line."""
        if len(self.storage) < self.size:
            self.storage.extend(self.next_batch)
            # Schedule next product on the line
            if len(self.line) > 0:
                time, self.next_batch = self.line.pop()
                self.factory.schedule(time, self.put_in_crate)

            # If we have a full storage, try activate all receivers
            if len(self.storage) == self.size:
                for machine in self.receivers:
                    if machine.status == BORED:
                        self.factory.schedule(0, machine.start_producing)
        else:
            self.halted = True

    def remove_product(self, amount=1):
        if self.halted:
            self.factory.schedule(0, self.put_in_crate)
        return super().remove_product(amount)


if __name__ == '__main__':
    import gui
    print('buffers main')
    gui.main()
