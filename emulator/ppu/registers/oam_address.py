class OAMADDR:

    def __init__(self, ppu):
        self.ppu = ppu
        self.reg = 0

    # The register value remains unchanged after reset
    def reset(self):
        pass

    # Write-only
    def read(self):
        return self.reg

    def write(self, value):
        self.reg = value

    def increment(self):
        if(self.ppu.ppucontrol.isVRAMAdressIncrement32):
            self.reg += 32
        else:
            self.reg += 1
