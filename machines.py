"""This module contains the machine classes."""
from buffers import Buffer
from random import expovariate as exp, choice
from samples import samplesA, samplesB, samplesD

BUSY = 0
BORED = 1
BROKEN = 2
REPAIRING = 3
REPAIRING_DOUBLE = 3

#
# Abstract base class
#
class Machine:
    """abstract"""
    status = BORED
    total_produced = 0

    def __init__(self, buffer, factory, next_class_type):
        self.buffer = buffer
        self.factory = factory
        self.factory.schedule(self.lifetime_duration(), self.start_repair)
        self.next_class_type = next_class_type

    def __str__(self):
        return '{}\n total_produced: {}'.format(self.__class__.__name__, self.total_produced)

    def production_duration(self):
        raise NotImplementedError('Production duration not defined')

    def lifetime_duration(self):
        raise NotImplementedError('Lifetime duration not defined')

    def repair_duration(self):
        raise NotImplementedError('Repair duration not defined')

    def start_producing(self):
        self.status = BUSY
        self.factory.schedule(self.production_duration(), self.finish_producing)

    def finish_producing(self):
        # If the machine is broken, the current item he's working on is thrown away
        if self.status != BUSY:
            return
        # When the machine is OK, update the stats to say the DVD is produced
        self.status = BORED
        try:
            self.buffer.add_product()
        except:
            pass # Discard the produced DVD isntead of passing it on to the buffer
        else:
            self.total_produced += 1
            self.start_producing()

    def start_repair(self):
        """In the case of a breakdown, try to start repairing."""
        if False:
            self.status = REPAIRING_DOUBLE  # Not sure right now
        if self.factory.available_repairmen > 0:
            self.status = REPAIRING
            self.factory.schedule(self.repair_duration(), self.end_repair)
        else:
            self.status = BROKEN

    def end_repair(self):
        """Finish the repairing of the machine."""
        # Dismiss the repair guy(s)
        self.factory.add_repairman()
        if self.status == REPAIRING_DOUBLE:
            self.factory.add_repairman()
        # Give the machine something to do again
        self.status = BORED
        self.start_producing()
        # Schedule a new breakdown
        self.factory.schedule(self.lifetime_duration, self.start_repair)


#
# Actual instances of the base class
#
class MachineA(Machine):
    def __init__(self, factory):
        buffer = Buffer(self, factory)
        Machine.__init__(self, buffer, factory, MachineB)

    def production_duration(self):
        return choice(samplesA)

    def lifetime_duration(self):
        return 1337 # exp 8h

    def repair_duration(self):
        return 1337 # exp 2h


class MachineB(Machine):
    def __init__(self, factory):
        buffer = Buffer(self, factory)
        Machine.__init__(self, buffer, factory, MachineC)

    def production_duration(self):
        return choice(samplesB)

    def lifetime_duration(self):
        return 1337 # exp ?h

    def repair_duration(self):
        return 1337 # exp ?h


class MachineC(Machine):
    def __init__(self, factory):
        buffer = Buffer(self, factory)
        Machine.__init__(self, buffer, factory, MachineD)

    def production_duration(self):
        return 1337 # insert something here

    def lifetime_duration(self):
        return 1337 # exp ?h

    def repair_duration(self):
        return 1337 # exp ?h


class MachineD(Machine):
    def __init__(self, factory):
        buffer = Buffer(self, factory)
        Machine.__init__(self, buffer, factory, None)

    def production_duration(self):
        return choice(samplesD)

    def lifetime_duration(self):
        return 1337 # exp ?h

    def repair_duration(self):
        return 1337 # exp ?h

