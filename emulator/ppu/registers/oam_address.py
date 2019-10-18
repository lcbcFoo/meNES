class OAMADDR:

    def __init__(self, ppu):
        self.ppu = ppu
        self.reg = 0

    # The register value remains unchanged after reset
    def reset(self):
        pass

    # Write-only
    def read(self):
        pass

    def write(self, value):
        self.reg = value
