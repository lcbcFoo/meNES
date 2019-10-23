class OAMDATA:

    def __init__(self, ppu):
        self.ppu = ppu

    def reset(self):
        pass

    def read(self):
        OAMaddr = self.ppu.oamaddr.reg
        return self.ppu.mem_bus.read(OAMaddr)

    def write(self, value):
        self.reg = value
        OAMaddr = self.ppu.oamaddr.reg
        self.ppu.mem_bus.write(OAMaddr, value)
        self.ppu.oamaddr.increment()
