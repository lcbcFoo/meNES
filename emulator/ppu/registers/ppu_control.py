class PPUCTRL:

    NMI_BIT = 7
    SLAVE_BIT = 6
    SPRITE_HEIGHT_BIT = 5
    BACKGROUND_PATTERN_TABLE_BIT = 4
    SPRITE_PATTERN_TABLE_BIT = 3
    VRAM_ADDRESS_INCREMENT_BIT = 2
    BASE_TABLE_ADDRESSH = 1
    BASE_TABLE_ADDRESSL = 0

    def __init__(self, ppu):
        self.ppu = ppu
        self.reset()

    def reset(self):
        self.reg = 0

    # Write-only
    def read(self):
        return self.reg

    def write(self,value):
        self.reg = value

    def isNMIEnabled():
        return (1 << NMI_BIT) & self.reg

    def isSpriteH16():
        return (1 << SPRITE_HEIGHT_BIT) & self.reg

    def isBackgroundPatternTable1000():
        return (1 << BACKGROUND_PATTERN_TABLE_BIT) & self.reg

    def isSpritePatternTable1000():
        return (1 << SPRITE_PATTERN_TABLE_BIT) & self.reg

    def isVRAMAdressIncrement32():
        return (1 << VRAM_ADDRESS_INCREMENT_BIT) & self.reg

    def returnNameTableAddress():
        highbit = (1 << BASE_TABLE_ADDRESSH) & self.reg
        lowbit = (1 << BASE_TABLE_ADDRESSL) & self.reg
        return highbit + lowbit
