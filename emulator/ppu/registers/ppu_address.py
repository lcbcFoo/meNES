class PPUADDR:

    def __init__(self, ppu):
        self.ppu = ppu
        self.reg = 0
        self.firstwrite = True

    def reset(self):
        self.firstwrite = True

    def read(self):
        return self.reg

    def write(self, value):
        if(self.firstwrite):
            self.reg = (value << 8)
        else:
            self.reg += (value)

        self.firstwrite = not self.firstwrite

    def increment(self):
        if(self.ppu.ppucontrol.isVRAMAdressIncrement32):
            self.reg += 32
        else:
            self.reg += 1
