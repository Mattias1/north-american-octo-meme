"""This module contains the machine classes."""
BUSY = 'busy'
BORED = 'bored'
BROKEN = 'broken'
REPAIRING = 'repairing'
REPAIRING_DOUBLE = 'repairing_double'

from buffers import Buffer
from random import expovariate as exp, normalvariate as normal, choice, randint
from samples import samplesA, samplesB, samplesD


class Machine:
    """Abstract base class for machines"""
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
            if provider.storage > 0:
                provider.remove_product()
                self.status = BUSY
                self.factory.schedule(self.production_duration(), self.finish_producing)
                return

    def finish_producing(self):
        # NOTE: If the machine is broken, the current item he's working on is thrown away
        if self.status != BUSY:
            return

        self.status = BORED
        if self.buffer.storage < self.buffer.size:
            self.buffer.add_product()
            self.total_produced += 1
            # NOTE: Low priority - must be lower than the one in
            # MachineC.finish_producing and machineD.finish_producing
            self.factory.schedule(0, self.start_producing, 0)

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
# Actual instances of the Machine base class
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
        # Exponential distribution with a mean of 8 hours
        return exp(1 / (8 * 3600))

    def repair_duration(self):
        # Exponential distribution with a mean of 2 hours
        return exp(1 / (2 * 3600))


class MachineB(Machine):
    def production_duration(self):
        return choice(samplesB)

    def lifetime_duration(self):
        # This machine doesnt break like that.
        # It sometimes loses a DVD and just has to start over.
        return -1

    def repair_duration(self):
        raise Exception("This machine (B) doesn't break like that")

    def finish_producing(self):
        # Discard DVD in 2% of the cases
        if randint(1, 100) <= 2:
            self.status = BORED
            self.factory.schedule(0, self.start_producing)
            return
        super().finish_producing()


class MachineC(Machine):
    def production_duration(self):
        return 5  # insert something here

    def lifetime_duration(self):
        return -1  # This crashes every 3% of the DVD's

    def repair_duration(self):
        return 5 * 60  # 5 minutes exactly

    def finish_producing(self):
        super().finish_producing()
        # Cleaning after producion of 3% of the DVD's
        if randint(1, 100) <= 3:
            # Priority must be higher than the start producing scheduled in the super.finish_producing
            self.factory.schedule(0, self.start_repair, 9)


class MachineD(Machine):
    def __init__(self, factory):
        buffer = Buffer(factory, float('inf'))
        Machine.__init__(self, factory, buffer)
        self.last_produced_count_replace_ink = self.total_produced
        self.next_dif_replace_ink = self.ink_replace_nr()

    def production_duration(self):
        return choice(samplesD)

    def lifetime_duration(self):
        return -1  # This machine doesnt break like that, it sometimes loses a DVD and just has to start over

    def repair_duration(self):
        # Normal deviation with avg 15 min and dev 1 min
        return normal(15 * 60, 1 * 60)

    def finish_producing(self):
        super().finish_producing()
        dif = self.total_produced - self.last_produced_count_replace_ink
        if self.total_produced - self.last_produced_count_replace_ink == self.next_dif_replace_ink:
            # Priority must be higher than the start producing scheduled in the super.finish_producing
            self.factory.schedule(0, self.start_repair, 9)

    def end_repair(self):
        super().end_repair()
        self.last_produced_count_replace_ink = self.total_produced
        self.next_dif_replace_ink = self.ink_replace_nr()

    def ink_replace_nr(self):
        p = randint(1, 100)
        if p <= 40:
            return 200
        if p <= 60:
            return 199
        if p <= 80:
            return 201
        if p <= 90:
            return 198
        return 202


if __name__ == '__main__':
    import gui
    print('machines main')
    gui.main()
