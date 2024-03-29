class PPUSCROLL:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reset()

    def reset(self):
        self.reg.store(0)
        self.x = 0
        self.y = 0
        self.firstwrite = True

    # Write-only
    def read(self, sys):
        # if sys:
        #     return 0
        return self.reg.load()

    def write(self, value, sys):
        if sys:
            return
        self.reg.store(value)

        #See how it works in the wiki
        if(self.firstwrite):
            self.x = value
        else:
            self.y = value

        self.firstwrite = not self.firstwrite
