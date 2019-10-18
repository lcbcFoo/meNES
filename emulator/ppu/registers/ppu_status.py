class PPUSTATUS:
    VBLANK_STATUS_BIT = 7
    SPRITE0_HIT_BIT = 6
    SPRITE_OVERFLOW_BIT = 5

    # I do not know how to decide the initial value to the register.
    # Ask the teacher about it
    def __init__(self, ppu):
        self.ppu = ppu
        self.reg = 0

    def reset(self):
        pass

    def read(self):
        value = self.reg
        self.reg = ~(1 << VBLANK_STATUS_BIT) & self.reg
        return self.reg

    def write(self, value):
        self.reg = self.reg & 0b11100000
        tempvalue = value & 0b00011111
        self.reg = self.reg + tempvalue

    def hasVblankStarted():
        return (1 << VBLANK_STATUS_BIT) & self.reg

    def isSprite0Hit():
        return (1 << SPRITE0_HIT_BIT) & self.reg

    def isSpriteOverflowSet():
        return (1 << SPRITE_OVERFLOW_BIT) & self.reg
