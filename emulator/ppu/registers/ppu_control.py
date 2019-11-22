NMI_BIT = 7
SLAVE_BIT = 6
SPRITE_HEIGHT_BIT = 5
BACKGROUND_PATTERN_TABLE_BIT = 4
SPRITE_PATTERN_TABLE_BIT = 3
VRAM_ADDRESS_INCREMENT_BIT = 2
BASE_TABLE_ADDRESSH = 1
BASE_TABLE_ADDRESSL = 0

class PPUCTRL:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reset()

    def reset(self):
        self.reg.store(0)

    # Write-only
    def read(self, sys):
        # if sys:
        #     return 0
        return self.reg.load()

    def write(self,value, sys):
        if sys:
            return
        self.reg.store(value)

    def isNMIEnabled(self):
        return self.reg.isBitSet(NMI_BIT)

    def isSpriteH16(self):
        return self.reg.isBitSet(SPRITE_HEIGHT_BIT)

    def isBackgroundPatternTable1000(self):
        return self.reg.isBitSet(BACKGROUND_PATTERN_TABLE_BIT)

    def isSpritePatternTable1000(self):
        return self.reg.isBitSet(SPRITE_PATTERN_TABLE_BIT)

    def isVRAMAdressIncrement32(self):
        return self.reg.isBitSet(VRAM_ADDRESS_INCREMENT_BIT)

    def returnNameTableAddress(self):
        highbit = self.reg.loadBit(BASE_TABLE_ADDRESSH)
        lowbit = self.reg.loadBit(BASE_TABLE_ADDRESSL)
        # (0 = $2000; 1 = $2400; 2 = $2800; 3 = $2C00)
        return 0x2000 + (highbit * 2 + lowbit) * 0x400
