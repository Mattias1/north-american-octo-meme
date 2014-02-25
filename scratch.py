from queue import PriorityQueue


class EventQueue(PriorityQueue):
    cur_time = 0
    def start(self):
        pass

simulation = EventQueue()
def schedule(time, handler):
    simulation.put((simulation.cur_time + time, handler))

class BufferAB:
    def add_product(self):
        pass

class MachineA:
    buffer = BufferAB()

    def produce(self):
        # update stats
        schedule(0, self.buffer.add_product)
        schedule(0, self.produce)

simulation.start()
