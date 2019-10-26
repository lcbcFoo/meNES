class OAMADDR:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reg.store(0)

    # The register value remains unchanged after reset
    def reset(self):
        pass

    # Write-only
    def read(self):
        return self.reg.load()

    def write(self, value):
        self.reg.store(value)

    def increment(self):
        self.reg.store(self.reg.increment())
