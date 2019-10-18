class PPUCTRL:
    NMI_BIT = 7
    SLAVE_BIT = 6
    SPRITE_HEIGHT_BIT = 5
    BACKGROUND_PATTERN_TABLE_BIT = 4
    SPRITE_PATTERN_TABLE_BIT = 3
    VRAM_ADDRESS_INCREMENT_BIT = 2
    BASE_TABLE_ADDRESS = 0

    def __init__(self, ppu):
        self.ppu = ppu
        self.reset()

    def reset(self):
        self.reg = 0

    def read(self):
        pass

    def write(self,value):
        self.reg = value
        pass
