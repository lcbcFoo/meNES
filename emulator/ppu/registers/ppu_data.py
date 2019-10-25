class PPUDATA:

    def __init__(self, ppu):
        self.ppu = ppu
        self.register = register
        self.reset()

    def reset(self):
        self.reg.store(0)

    def read(self):
        VRAMaddr = self.ppu.ppuaddr.reg.load()
        self.ppu.ppuaddr.increment()
        self.reg.write(self.ppu.mem_bus.read(VRAMaddr))
        return self.reg.load()

    def write(self, value):
        self.reg.write(value)
        VRAMaddr = self.ppu.ppuaddr.reg.load()
        self.ppu.mem_bus.write(VRAMaddr, value)
        self.ppu.ppuaddr.increment()
