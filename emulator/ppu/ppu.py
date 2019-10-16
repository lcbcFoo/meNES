import sys

class PPU:

    def __init__(self, bus):
        self.mem_bus = bus
        self.reset()

    def reset(self):
        pass

    def run(self):
        pass

    def write(self, addr, value):
        pass

    def read(self, addr):
        return 0
