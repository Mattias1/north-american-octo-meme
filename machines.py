"""This module contains the machine classes."""
BUSY = 'busy'
BORED = 'idle'
BROKEN = 'broken'
REPAIRING = 'repairing'
REPAIRING_DOUBLE = 'repairing_double'

from buffers import Buffer
from random import expovariate as exp, normalvariate as normal, randint, random
from samples import samplesA, samplesB, samplesD


class Machine:
    """Abstract base class for machines"""
    _status = BORED
    old_status_time = 0
    has_discarded = False
    total_produced = 0
    total_discarded = 0
    total_busy_time = 0
    total_bored_time = 0
    total_down_time = 0
    batchsize = 1
    breakdowns = 0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        # If the status doesn't actually change, don't do anything.
        if self._status == value:
            return
        # If the machine is no longer busy
        if self._status == BUSY:
            self.total_busy_time += self.factory.cur_time - self.old_status_time
            self.old_status_time = self.factory.cur_time
        # If the machine is no longer bored
        if self._status == BORED:
            self.total_bored_time += self.factory.cur_time - self.old_status_time
            self.old_status_time = self.factory.cur_time
        # If the machine is no longer down
        down = [BROKEN, REPAIRING, REPAIRING_DOUBLE]
        if self._status in down and value not in down:
            self.total_down_time += self.factory.cur_time - self.old_status_time
            self.old_status_time = self.factory.cur_time
        # Finally set the new value
        self._status = value

    def __init__(self, factory, providers, receivers):
        self.stats = {}
        self.providers = providers
        self.receivers = receivers
        self.factory = factory
        self.batch = []

        duration = self.lifetime_duration()
        if duration != -1:
            self.factory.schedule(duration, self.start_repair)

    def update_stats(self):
        self.stats['status'] = self.status
        self.stats['total_produced'] = self.total_produced * self.batchsize
        self.stats['total_discarded'] = self.total_discarded
        self.stats['receivers_storage'] = sum([len(r.storage) for r in self.receivers])
        self.stats['breakdowns'] = self.breakdowns
        self.stats['time_busy'] = self.total_busy_time / (60 * 60)
        self.stats['time_bored'] = self.total_bored_time / (60 * 60)
        self.stats['time_down'] = self.total_down_time / (60 * 60)

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
            if len(provider.storage) >= self.batchsize:
                self.batch = provider.remove_product(self.batchsize)
                self.status = BUSY
                self.factory.schedule(self.production_duration(), self.finish_producing)
                return

    def finish_producing(self):
        # If machine has been broken, the current item is thrown away
        if self.has_discarded:
            self.has_discarded = False
            self.batch = []
            return

        if self.status != BUSY:
            # apparently BORED
            return

        self.status = BORED
        for buffer in self.receivers:
            if buffer.enough_room(self.batchsize):
                buffer.add_product(self.batch)
                self.total_produced += 1
                # NOTE: Low priority - must be lower than the one in
                # MachineC.finish_producing and machineD.finish_producing
                self.factory.schedule(0, self.start_producing, 0)
                return

    def start_repair(self):
        """In the case of a breakdown, try to start repairing."""
        assert self.status != REPAIRING and self.status != REPAIRING_DOUBLE

        self.breakdowns += 1
        if self.status == BUSY:
            self.total_discarded += 1
            self.has_discarded = True

        if self.factory.available_repairmen > 0:
            self.factory.available_repairmen -= 1
            self.status = REPAIRING
            if self.double_repair() and self.factory.available_repairmen > 0:
                self.factory.available_repairmen -= 1
                self.status = REPAIRING_DOUBLE
            self.factory.schedule(self.repair_duration(), self.end_repair)
        else:
            self.status = BROKEN

    def end_repair(self):
        """Finish the repairing of the machine."""
        assert self.status in [REPAIRING, REPAIRING_DOUBLE]

        # Dismiss the repair guy(s)
        if self.status == REPAIRING_DOUBLE:
            self.factory.add_repairman(2)
        else:
            self.factory.add_repairman()

        # Give the machine something to do again
        self.status = BORED
        self.factory.schedule(0, self.start_producing)

        # Schedule a new breakdown
        duration = self.lifetime_duration()
        if duration != -1:
            self.factory.schedule(duration, self.start_repair)

    def double_repair(self):
        """Whether or not we need two repair guys for the machine."""
        return False


#
# Actual instances of the Machine base class
#
class MachineA(Machine):
    def __init__(self, factory, receivers):
        Machine.__init__(self, factory, [], receivers)

    def start_producing(self):
        if self.status != BORED:
            return
        # MachineA has no providers
        self.status = BUSY
        self.factory.schedule(self.production_duration(), self.finish_producing)
        self.batch = [self.factory.cur_time]

    def production_duration(self):
        return interpolate_samples(samplesA)

    def lifetime_duration(self):
        # Exponential distribution with a mean of 8 hours
        return exp(1 / (8 * 3600))

    def repair_duration(self):
        # Exponential distribution with a mean of 2 hours
        return exp(1 / (2 * 3600))

    def double_repair(self):
        # 50% chance at needing two repair guys for a machine
        # 50% is chosen as the only thing we know is 'sometimes' - assumption (!)
        return randint(0, 1) == 0


class MachineB(Machine):
    def production_duration(self):
        return interpolate_samples(samplesB)

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
            self.total_discarded += 1
            self.factory.schedule(0, self.start_producing)
            return
        super().finish_producing()


class MachineC(Machine):
    def __init__(self, factory, providers, receivers, batchsize):
        self.batchsize = batchsize
        Machine.__init__(self, factory, providers, receivers)

    def production_duration(self):
        # One exponential with an average of 10 seconds,
        # plus another exponential with an average of 6 seconds, plus 3 minutes.
        return exp(1 / 10) + exp(1 / 6) + 3 * 60  # insert something here

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
    def __init__(self, factory, providers):
        buffer = Buffer(self, float('inf'))
        Machine.__init__(self, factory, providers, [buffer])
        self.last_produced_count_replace_ink = self.total_produced
        self.next_dif_replace_ink = self.ink_replace_nr()

    def production_duration(self):
        return interpolate_samples(samplesD)

    def lifetime_duration(self):
        return -1  # This machine doesnt break like that, it sometimes loses a DVD and just has to start over

    def repair_duration(self):
        # Normal deviation with avg 15 min and dev 1 min
        return normal(15 * 60, 1 * 60)

    def finish_producing(self):
        self.factory.throughputs.extend([self.factory.cur_time - dvd for dvd in self.batch])
        super().finish_producing()

        if self.total_produced - self.last_produced_count_replace_ink == self.next_dif_replace_ink:
            # Priority must be higher than the start producing scheduled in the super.finish_producing
            self.factory.schedule(0, self.start_repair, 9)

    def end_repair(self):
        super().end_repair()
        self.last_produced_count_replace_ink = self.total_produced
        self.next_dif_replace_ink = self.ink_replace_nr()

    @staticmethod
    def ink_replace_nr():
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


def interpolate_samples(samples):
    # Assumes samples to be sorted in ascending order
    i = randint(0, len(samples) - 2)
    r = random()
    return samples[i] + r * (samples[i + 1] - samples[i])

if __name__ == '__main__':
    import gui
    print('machines main')
    gui.main()
