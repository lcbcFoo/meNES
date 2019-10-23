class OAMDMA:

    def __init__(self, ppu):
        self.ppu = ppu
        self.reg = 0

    def reset(self):
        self.reg = 0

    def read(self):
        return self.reg

    def write(self, value):
        self.reg = value
