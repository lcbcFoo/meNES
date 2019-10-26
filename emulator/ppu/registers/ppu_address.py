class PPUADDR:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reg.store(0)
        self.firstwrite = True

    def reset(self):
        self.firstwrite = True

    def read(self):
        return self.reg.load()

    def write(self, value):
        if(self.firstwrite):
            self.reg.storeHigherByte(value)
        else:
            self.reg.storeLowerByte(value)

        self.firstwrite = not self.firstwrite

    def increment(self):
        if(self.ppu.ppuctrl.isVRAMAdressIncrement32):
            self.reg.add(32)
        else:
            self.reg.increment()
