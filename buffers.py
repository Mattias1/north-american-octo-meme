"""This module contains the classes for buffers."""
from machines import BORED
from collections import deque


class Buffer:
    storage = 0

    def __init__(self, factory, size):
        self.factory = factory
        assert size > 0
        self.size = size
        self.providers = []
        self.receivers = []

    def enough_room(self, amount=1):
        return self.storage + amount <= self.size

    def add_product(self, amount=1):
        if self.storage + amount <= self.size:
            self.storage += amount
            # Since we have a non empty storage, try to activate all receivers
            for machine in self.receivers:
                if machine.status == BORED:
                    self.factory.schedule(0, machine.start_producing)
        else:
            raise Exception('Buffer overflow.')

    def remove_product(self, amount=1):
        if self.storage >= amount:
            self.storage -= amount
            # Since we have a non full storage, try to activate all providers
            for machine in self.providers:
                if machine.status == BORED:
                    machine.start_producing()
        else:
            raise Exception('Buffer underflow.')


class AssemblyLine(Buffer):
    halted = False

    def __init__(self, factory, size):
        super().__init__(factory, size)
        self.line = deque()

    def add_product(self, amount=1):
        if self.enough_room():
            self.put_on_line()
        else:
            raise Exception('Assembly line overflow.')

    def put_on_line(self):
        """Puts product on assembly line."""
        total_queue_time = sum(self.line)
        assert total_queue_time <= 5
        self.line.appendleft(5 - total_queue_time)
        self.halted = False

        if len(self.line) == 1:
            self.factory.schedule(5, self.put_in_crate)

    def put_in_crate(self):
        """Puts product in crate after assembly line."""
        if self.storage < self.size:
            self.storage += 1
            # Schedule next product on the line
            if len(self.line) > 0:
                self.factory.schedule(self.line.pop(), self.put_in_crate)

            # If we have a full storage, try activate all receivers
            if self.storage == self.size:
                for machine in self.receivers:
                    if machine.status == BORED:
                        self.factory.schedule(0, machine.start_producing)
        else:
            self.halted = True

    def remove_product(self, amount=1):
        super().remove_product(amount)
        if self.halted:
            self.factory.schedule(0, self.put_in_crate)

if __name__ == '__main__':
    import gui
    print('buffers main')
    gui.main()
