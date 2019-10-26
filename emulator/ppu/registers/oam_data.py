class OAMDATA:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register

    def reset(self):
        pass

    def read(self):
        OAMaddr = self.ppu.oamaddr.read()
        self.reg.store(self.ppu.mem_bus.read(OAMaddr))
        return self.reg.load()

    def write(self, value):
        self.reg.store(value)
        OAMaddr = self.ppu.oamaddr.read()
        self.ppu.mem_bus.write(OAMaddr, value)
        self.ppu.oamaddr.increment()
