class OAMDATA:

    def __init__(self, ppu):
        self.ppu = ppu

    def reset(self):
        pass

    def read(self, ppu):
        OAMaddr = ppu.oamaddr.reg
        return ppu.mem_bus.read(OAMADDR)

    def write(self, value):
        self.reg = value
        OAMaddr = self.ppu.oamaddr.reg
        self.ppu.mem_bus.write(OAMADDR, value)
        self.ppu.oamaddr.reg += 1
