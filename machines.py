"""This module contains the machine classes."""
BUSY = 'busy'
BORED = 'bored'
BROKEN = 'broken'
REPAIRING = 'repairing'
REPAIRING_DOUBLE = 'repairing_double'

from buffers import BufferSizeExceeding, Buffer
from random import expovariate as exp, choice, randint
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
        self.stats = {}
        self.providers = []

        duration = self.lifetime_duration()
        if duration != -1:
            self.factory.schedule(duration, self.start_repair)

    def update_stats(self):
        self.stats['status'] = self.status
        self.stats['total_produced'] = self.total_produced
        self.stats['buffer_storage'] = self.buffer.storage

    def production_duration(self):
        raise NotImplementedError('Production duration is abstract')

    
    def lifetime_duration(self):
        raise NotImplementedError('Lifetime duration is abstract')

    def repair_duration(self):
        raise NotImplementedError('Repair duration is abstract')

    def start_producing(self):
        if self.status != BORED:
            return
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
            self.factory.schedule(0, self.start_producing, 0) # Low priority - must be lower than the one in MachineC.finish_producing

    def start_repair(self):
        """In the case of a breakdown, try to start repairing."""
        if False:
            self.status = REPAIRING_DOUBLE  # Not sure right now
        if self.factory.available_repairmen > 0:
            self.factory.available_repairmen -= 1
            self.status = REPAIRING
            self.factory.schedule(self.repair_duration(), self.end_repair)
        else:
            self.status = BROKEN

    def end_repair(self):
        """Finish the repairing of the machine."""
        # Dismiss the repair guy(s)
        self.factory.add_repairman()
        if self.status == REPAIRING_DOUBLE:
            self.factory.schedule(0, self.factory.add_repairman)
        # Give the machine something to do again
        self.status = BORED
        self.factory.schedule(0, self.start_producing)
        # Schedule a new breakdown
        duration = self.lifetime_duration()
        if duration != -1:
            self.factory.schedule(duration, self.start_repair)


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
        return exp(1 / (8*3600)) # Exponential distribution with a mean of 8 hours

    def repair_duration(self):
        return exp(1 / (2*3600)) # Exponential distribution with a mean of 2 hours


class MachineB(Machine):
    def production_duration(self):
        return choice(samplesB)

    def lifetime_duration(self):
        return -1 # This machine doesnt break like that, it sometimes loses a DVD and just has to start over

    def repair_duration(self):
        raise Exception("This machine (B) doesn't break like that")

    def finish_producing(self):
        # Discard DVD in 2% of the cases
        if randint(1, 100) <= 2:
            self.factory.schedule(0, self.start_producing)
            return
        super().finish_producing()


class MachineC(Machine):
    def production_duration(self):
        return 5 # insert something here

    def lifetime_duration(self):
        return -1 # This crashes every 3% of the DVD's

    def repair_duration(self):
        return 5*60 # 5 minutes exactly

    def finish_producing(self):
        super().finish_producing()
        # Cleaning after producion of 3% of the DVD's
        if randint(1,100) <= 3:
            self.factory.schedule(0, self.start_repair, 9) # Priority must be higher than the start producing scheduled in the super.finish_producing


class MachineD(Machine):
    def __init__(self, factory):
        buffer = Buffer(factory, float('inf'))
        Machine.__init__(self, factory, buffer)

    def production_duration(self):
        return choice(samplesD)

    def lifetime_duration(self):
        return 1337 # 200 DVD's, with weird distribution for +-2 or +- 1

    def repair_duration(self):
        return 1337 # standard avg 15 min dev 1 min


if __name__ == '__main__':
    import gui
    print('machines main')
    gui.main()
