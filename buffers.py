"""This module contains the classes for buffers."""
from machines import BORED


class Buffer:
    """This class has no docstring."""
    storage = 0

    def __init__(self, factory, size):
        self.factory = factory
        assert size > 0
        self.size = size
        self.providers = []
        self.receivers = []

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
    def add_product(self, amount):
        self.put_on_line()

    def put_on_line(self):
        """Puts product on assembly line."""
        self.factory.schedule(5, self.put_in_crate)

    def put_in_crate(self):
        """Puts product in crate after assembly line."""
        Buffer.add_product(self)


if __name__ == '__main__':
    import gui
    print('buffers main')
    gui.main()
