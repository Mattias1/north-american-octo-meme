"""This module contains the classes for buffers."""
from machines import BORED


class BufferSizeExceeding(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)


class Buffer:
    """This class has no docstring."""
    storage = 0

    def __init__(self, factory, size):
        self.factory = factory
        assert size > 0
        self.size = size
        self.providers = []
        self.receivers = []

    def add_product(self):
        if self.storage < self.size:
            self.storage += 1
            # Since we have a non empty storage, try to activate all receivers
            for machine in self.receivers:
                if machine.status == BORED:
                    self.factory.schedule(0, machine.start_producing)
        else:
            raise BufferSizeExceeding('Buffer overflow.')

    def remove_product(self):
        if self.storage > 0:
            self.storage -= 1
            # Since we have a non full storage, try to activate all providers
            for machine in self.providers:
                if machine.status == BORED:
                    machine.start_producing()
        else:
            raise BufferSizeExceeding('Buffer underflow.')


if __name__ == '__main__':
    import gui
    print('buffers main')
    gui.main()
