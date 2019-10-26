class OAMDMA:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reg.store(0)

    def reset(self):
        self.reg = 0

    def read(self):
        return self.reg.load()

    def write(self, value):
        self.reg.store(value)
