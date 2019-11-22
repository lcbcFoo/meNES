EMPHASIZE_BLUE_BIT = 7
EMPHASIZE_GREEN_BIT = 6
EMPHASIZE_RED_BIT = 5
SHOW_SPRITE_BIT = 4
SHOW_BACKGROUND_BIT = 3
SHOW_LEFTMOST_SPRITE_BIT = 2
SHOW_LEFTMOST_BACKGROUND_BIT = 1
GREYSCALE_BIT = 0

class PPUMASK:

    def __init__(self, ppu, register):
        self.ppu = ppu
        self.reg = register
        self.reset()

    def reset(self):
        self.reg.store(0)

    def read(self, sys):
        # if sys:
        #     return 0
        return self.reg.load()

    def write(self, value, sys):
        if sys:
            return
        self.reg.store(value)

    def isEmphasizeBlueEnabled(self):
        return self.reg.isBitSet(EMPHASIZE_BLUE_BIT)

    def isEmphasizeGreenEnabled(self):
        return self.reg.isBitSet(EMPHASIZE_GREEN_BIT)

    def isEmphasizeRedEnabled(self):
        return self.reg.isBitSet(EMPHASIZE_RED_BIT)

    def isSpriteEnabled(self):
        return self.reg.isBitSet(SHOW_SPRITE_BIT)

    def isBackgroundEnabled(self):
        return self.reg.isBitSet(SHOW_BACKGROUND_BIT)

    def isLeftmostSpriteEnabled(self):
        return self.reg.isBitSet(SHOW_LEFTMOST_SPRITE_BIT)

    def isLeftmostBackgroundEnabled(self):
        return self.reg.isBitSet(SHOW_LEFTMOST_BACKGROUND_BIT)

    def isGrayScaleEnabled(self):
        return self.reg.isBitSet(GREYSCALE_BIT)
