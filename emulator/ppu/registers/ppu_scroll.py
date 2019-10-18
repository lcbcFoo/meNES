class PPUSCROLL:

    def __init__(self, ppu):
        self.ppu = ppu
        self.reset()

    def reset(self):
        self.reg = 0
        self.firstwrite = True

    # Write-only
    def read(self):
        pass

    def write(self, value):
        self.reg = value

        #See how it works in the wiki
        if(self.firstwrite):
            pass
        else:
            pass

        self.firstwrite = not self.firstwrite
