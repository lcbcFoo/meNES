class PPUSCROLL:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reset()

    def reset(self):
        self.reg.store(0)
        self.firstwrite = True

    # Write-only
    def read(self):
        return self.reg.load()

    def write(self, value):
        self.reg.write(value)

        #See how it works in the wiki
        if(self.firstwrite):
            pass
        else:
            pass

        self.firstwrite = not self.firstwrite
