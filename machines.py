"""This module contains the machine classes."""
BUSY = 'busy'
BORED = 'bored'
BROKEN = 'broken'
REPAIRING = 'repairing'
REPAIRING_DOUBLE = 'repairing_double'

from buffers import BufferSizeExceeding, Buffer
from random import expovariate as exp, choice
from samples import samplesA, samplesB, samplesD

#
# Abstract base class
#
class Machine:
    """abstract"""
    status = BORED
    total_produced = 0

    def __init__(self, factory, buffer):
        self.stats = {}
        self.providers = []
        self.factory = factory
        self.buffer = buffer

        self.factory.schedule(self.lifetime_duration(), self.start_repair)

    def update_stats(self):
        self.stats['status'] = self.status
        self.stats['total_produced'] = self.total_produced
        self.stats['buffer_storage'] = self.buffer.storage

    def production_duration(self):
        raise NotImplementedError('Production duration is abstract')

    
        raise NotImplementedError('Lifetime duration is abstract')

    def repair_duration(self):
        raise NotImplementedError('Repair duration is abstract')

    def start_producing(self):
        for provider in self.providers:
            try:
                provider.remove_product()
            except BufferSizeExceeding:
                pass
            else:
                self.status = BUSY
                self.factory.schedule(self.production_duration(), self.finish_producing)
                return

    def finish_producing(self):
        # If the machine is broken, the current item he's working on is thrown away
        if self.status != BUSY:
            return
        # When the machine is OK, update the stats to say the DVD is produced
        self.status = BORED
        try:
            self.buffer.add_product()
        except BufferSizeExceeding:
            # Discard the produced DVD instead of passing it on to the buffer
            pass
        else:
            self.total_produced += 1
            self.factory.schedule(0, self.start_producing)

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
        assert False
        """Finish the repairing of the machine."""
        # Dismiss the repair guy(s)
        self.factory.add_repairman()
        if self.status == REPAIRING_DOUBLE:
            self.factory.schedule(0, self.factory.add_repairman)
        # Give the machine something to do again
        self.status = BORED
        self.factory.schedule(0, self.start_producing)
        # Schedule a new breakdown
        self.factory.schedule(self.lifetime_duration(), self.start_repair)


#
# Actual instances of the base class
#
class MachineA(Machine):
    def start_producing(self):
        # MachineA has no providers
        self.status = BUSY
        self.factory.schedule(self.production_duration(), self.finish_producing)

    def production_duration(self):
        # TODO: don't use samples, but interpolate between the sorted list of samples
        return choice(samplesA)

    def lifetime_duration(self):
        return 1337 # exp 8h

    def repair_duration(self):
        return 1337 # exp 2h


class MachineB(Machine):
    def production_duration(self):
        return choice(samplesB)

    def lifetime_duration(self):
        return 1337 # exp ?h

    def repair_duration(self):
        return 1337 # exp ?h


class MachineC(Machine):
    def production_duration(self):
        return 5 # insert something here

    def lifetime_duration(self):
        return 1337 # exp ?h

    def repair_duration(self):
        return 1337 # exp ?h


class MachineD(Machine):
    def __init__(self, factory):
        buffer = Buffer(factory, float('inf'))
        Machine.__init__(self, factory, buffer)

    def production_duration(self):
        return choice(samplesD)

    def lifetime_duration(self):
        return 1337 # exp ?h

    def repair_duration(self):
        return 1337 # exp ?h


if __name__ == '__main__':
    import gui
    print('machines main')
    gui.main()
