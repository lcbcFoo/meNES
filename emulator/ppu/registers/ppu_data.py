class PPUDATA:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reset()

    def reset(self):
        self.reg.store(0)
        self.buffer = 0

    def read(self, sys):
        if sys:
            return 0

        data = self.buffer
        VRAMaddr = self.ppu.ppuaddr.reg.load()
        self.buffer = self.ppu.mem_bus.read(VRAMaddr)

        if(VRAMaddr >= 0x3F00):
            data = self.buffer

        self.ppu.ppuaddr.increment()
        self.reg.store(data)
        return data

    def write(self, value, sys):
        if sys:
            return
        self.reg.store(value)
        VRAMaddr = self.ppu.ppuaddr.reg.load()
        self.ppu.mem_bus.write(VRAMaddr, value)
        self.ppu.ppuaddr.increment()
