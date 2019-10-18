class PPUDATA:

    def __init__(self, ppu):
        self.ppu = ppu
        self.reg = 0

    def reset(self):
        self.reg = 0

    def read(self):
        VRAMaddr = self.ppu.ppuaddr.reg
        self.ppu.ppuaddr.increment()
        self.reg = self.ppu.mem_bus.read(VRAMaddr)
        return self.reg

    def write(self, value):
        self.reg = value
        VRAMaddr = self.ppu.ppuaddr.reg
        self.ppu.mem_bus.write(VRAMaddr, value)
        self.ppu.ppuaddr.increment()
