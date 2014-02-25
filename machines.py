"""This module contains the machine classes."""
from buffers import Buffer
from random import expovariate as exp, choice
from samples import samplesA

class Machine:
    """abstract"""
    def __init__(self, buffer, factory):
        self.buffer = buffer
        self.factory = factory

class MachineA(Machine):
    total_produced = 0

    def __init__(self, factory):
        buffer = Buffer(self, factory)
        Machine.__init__(self, buffer, factory)

    def __str__(self):
        return 'total_produced: {}'.format(self.total_produced)

    def start_producing(self):
        duration = choice(samplesA)
        self.factory.schedule(duration, self.finish_producing)

    def finish_producing(self):
        self.total_produced += 1
        try:
            self.buffer.add_product()
        except:
            self.stop()
        else:
            self.start_producing()

    def stop(self):
        pass

