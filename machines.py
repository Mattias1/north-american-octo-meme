"""This module contains the machine classes."""
from buffers import Buffer
from random import expovariate as exp, uniform

class Machine:
    """abstract"""
    def __init__(self, buffer, factory):
        self.buffer = buffer
        self.factory = factory

class MachineA(Machine):
    total_produced = 0

    def __init__(self, factory):
        buffer = Buffer(factory)
        Machine.__init__(self, buffer, factory)

    def __str__(self):
        return 'total_produced: {}'.format(self.total_produced)

    def start_producing(self):
        duration = uniform(0.8, 1.2)
        self.factory.schedule(duration, self.finish_producing)

    def finish_producing(self):
        self.total_produced += 1
        self.factory.schedule(0, self.buffer.add_product)
        self.factory.schedule(0, self.start_producing)

