class PPUSCROLL:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reset()
        self.my_flag = False

    def reset(self):
        self.reg.store(0)
        self.x = 0
        self.y = 0

    # Write-only
    def read(self, sys):
        # if sys:
        #     return 0
        return self.reg.load()

    def write(self, value, sys):
        if sys:
            return
        self.reg.store(value)
        # print("aqui")

        #See how it works in the wiki
        if(self.ppu.firstwrite):
            # print("atualizando o x: " + str(value))
            self.x = value
        else:
            # print("atualizando o y: " + str(value))
            self.y = value

        self.ppu.firstwrite = not self.ppu.firstwrite
