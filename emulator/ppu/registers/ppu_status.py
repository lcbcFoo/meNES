VBLANK_STATUS_BIT = 7
SPRITE0_HIT_BIT = 6
SPRITE_OVERFLOW_BIT = 5

class PPUSTATUS:

    # I do not know how to decide the initial value to the register.
    # Ask the teacher about it
    def __init__(self, ppu):
        self.ppu = ppu
        self.reg = register
        self.reg.store(0)

    def reset(self):
        pass

    def read(self):
        value = self.reg.load()
        self.reg.storeBit(VBLANK_STATUS_BIT, 0)
        self.ppu.ppuscroll.firstwrite = True
        self.ppu.ppuaddr.firstwrite = True
        return value

    def write(self, value):
        self.reg.storeBits(0, 5, value)

    def hasVblankStarted():
        return self.reg.isBitSet(VBLANK_STATUS_BIT)

    def isSprite0Hit():
        return self.reg.isBitSet(SPRITE0_HIT_BIT)

    def isSpriteOverflowSet():
        return self.reg.isBitSet(SPRITE_OVERFLOW_BIT)
