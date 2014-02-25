"""This module contains the classes for buffers."""

class Buffer:
    """This class has no docstring."""
    storage = 0
    size = 20
    def __init__(self, factory):
        self.factory = factory

    def add_product(self):
        self.storage += 1
        if self.storage >= self.size:
            self.factory.schedule(0, self.factory.stop)

