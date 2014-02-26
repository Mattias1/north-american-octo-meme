"""This module contains the machine classes."""
from buffers import Buffer
from random import expovariate as exp, choice
from samples import samplesA

BUSY = 0
BORED = 1
BROKEN = 2
REPAIRING = 3
REPAIRING_DOUBLE = 3


class Machine:
    """abstract"""
    status = BORED

    def __init__(self, buffer, factory):
        self.buffer = buffer
        self.factory = factory


class MachineA(Machine):
    total_produced = 0

    def __init__(self, factory):
        buffer = Buffer(self, factory)
        Machine.__init__(self, buffer, factory)

        duration = 1337  # Gem. om de 8 uur (exp)
        self.factory.schedule(duration, self.start_repair)

    def __str__(self):
        return 'total_produced: {}'.format(self.total_produced)

    def start_producing(self):
        duration = choice(samplesA)
        self.status = BUSY
        self.factory.schedule(duration, self.finish_producing)

    def finish_producing(self):
        # If the machine is broken, the current item he's working on is thrown away
        if self.status != BUSY:
            return
        # Otherwise, update the stats to say the DVD is produced
        self.status = BORED
        self.total_produced += 1
        try:
            self.buffer.add_product()
        except:
            self.stop()
        else:
            self.start_producing()

    def stop(self):
        pass

    def start_repair(self):
        """In the case of a breakdown, try to start repairing."""
        if False:
            self.status = REPAIRING_DOUBLE  # Not sure right now
        if self.factory.available_repairmen > 0:
            self.status = REPAIRING
            duration = 1337  # Gemiddeld 2 uur (exp)
            self.factory.schedule(duration, self.end_repair)
        else:
            self.status = BROKEN

    def end_repair(self):
        """Finish the repairing of the machine."""
        # Dismiss the repair guy(s)
        self.factory.schedule(0, self.factory.add_repairman)
        if self.status == REPAIRING_DOUBLE:
            self.factory.schedule(0, self.factory.add_repairman)
        # Give the machine something to do again
        self.status = BORED
        self.factory.schedule(0, self.start_producing)
        # Schedule a new breakdown
        duration = 1337  # Gem. om de 8 uur (exp)
        self.factory.schedule(duration, self.start_repair)
