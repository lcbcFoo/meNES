VBLANK_STATUS_BIT = 7
SPRITE0_HIT_BIT = 6
SPRITE_OVERFLOW_BIT = 5

class PPUSTATUS:

    # I do not know how to decide the initial value to the register.
    # Ask the teacher about it
    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reg.store(0)

    def reset(self):
        pass

    def read(self, sys):
        value_aux = self.reg.load() & 0xE0
        data_buffer = self.ppu.ppudata.buffer & 0x1F
        value = value_aux | data_buffer
        if not sys:
            self.reg.storeBit(VBLANK_STATUS_BIT, 0)
            # self.ppu.ppuscroll.firstwrite = True
            # self.ppu.ppuaddr.firstwrite = True
            self.ppu.firstwrite = True
        return value

    def write(self, value, sys):
        if sys:
            return
        self.reg.storeBits(0, 5, value)

    def hasVblankStarted(self):
        return self.reg.isBitSet(VBLANK_STATUS_BIT)

    def isSprite0Hit(self):
        return self.reg.isBitSet(SPRITE0_HIT_BIT)

    def isSpriteOverflowSet(self):
        return self.reg.isBitSet(SPRITE_OVERFLOW_BIT)
