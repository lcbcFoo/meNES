class OAMDMA:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reg.store(0)

    def reset(self):
        self.reg.store(0)

    def read(self, sys):
        if sys:
            return 0
        return self.reg.load()

    def write(self, value, sys):
        if sys:
            return
        self.reg.store(value)
        self.ppu.dma_on_going = True 
        self.ppu.dma_page = value
