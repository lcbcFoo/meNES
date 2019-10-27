class PPUDATA:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reset()

    def reset(self):
        self.reg.store(0)

    def read(self, sys):
        if sys:
            return 0
        VRAMaddr = self.ppu.ppuaddr.reg.load()
        self.ppu.ppuaddr.increment()
        self.reg.store(self.ppu.mem_bus.read(VRAMaddr))
        return self.reg.load()

    def write(self, value, sys):
        if sys:
            return
        self.reg.store(value)
        VRAMaddr = self.ppu.ppuaddr.reg.load()
        #print('ppu')
        #print(hex(VRAMaddr) + ' = ' + hex(value))

        self.ppu.mem_bus.write(VRAMaddr, value)
        self.ppu.ppuaddr.increment()
