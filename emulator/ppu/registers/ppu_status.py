class PPUSTATUS:
    VBLANK_STATUS_BIT = 7
    SPRITE0_HIT_BIT = 6
    SPRITE_OVERFLOW_BIT = 5

    # I do not know how to decide the initial value to the register.
    # Ask the teacher about it
    def __init__(self):
        self.reg = 0

    def read(self):
        value = self.reg
        self.reg = ~(1 << VBLANK_STATUS_BIT) & self.reg
        return self.reg
