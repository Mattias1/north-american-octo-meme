"""This module contains the classes for buffers."""

class Buffer:
    """This class has no docstring."""
    storage = 0
    size = 20

    def __init__(self, machine, factory):
        self.factory = factory
        self.machine = machine
        assert self.size > 0

    def add_product(self):
        if self.storage == 0:
            machine = self.factory.next_idle_machine(self.machine.next_class_type)
            if machine != None:
                self.factory.schedule(0, machine.start_producing)
                return
        if self.storage < self.size:
            self.storage += 1
        else:
            raise Exception('Buffer overflow.')

    def remove_product(self):
        if self.storage > 0:
            self.storage -= 1
            if True: # if exist machine that needs me
                pass # start that machine
        else:
            raise Exception('Buffer underflow.')


if __name__ == '__main__':
    import gui
    print('buffers main')
    gui.main()
