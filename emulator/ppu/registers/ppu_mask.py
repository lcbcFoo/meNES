class PPUMASK:

    EMPHASIZE_BLUE_BIT = 7
    EMPHASIZE_GREEN_BIT = 6
    EMPHASIZE_RED_BIT = 5
    SHOW_SPRITE_BIT = 4
    SHOW_BACKGROUND_BIT = 3
    SHOW_LEFTMOST_SPRITE_BIT = 2
    SHOW_LEFTMOST_BACKGROUND_BIT = 1
    GREYSCALE_BIT = 0

    def __init__(self, ppu):
        self.ppu = ppu
        self.reset()

    def reset(self):
        self.reg = 0

    def read(self):
        return self.reg

    def write(self, value):
        self.reg = value

    def isEmphasizeBlueEnabled():
        return (1 << EMPHASIZE_BLUE_BIT) & self.reg

    def isEmphasizeGreenEnabled():
        return (1 << EMPHASIZE_GREEN_BIT) & self.reg

    def isEmphasizeRedEnabled():
        return (1 << EMPHASIZE_RED_BIT) & self.reg

    def isSpriteEnabled():
        return (1 << SHOW_SPRITE_BIT) & self.reg

    def isBackgroundEnabled():
        return (1 << SHOW_BACKGROUND_BIT) & self.reg

    def isLeftmostSpriteEnabled():
        return (1 << SHOW_LEFTMOST_SPRITE_BIT) & self.reg

    def isLeftmostBackgroundEnabled():
        return (1 << SHOW_LEFTMOST_BACKGROUND_BIT) & self.reg

    def isGrayScaleEnabled():
        return (1 << GREYSCALE_BIT) & self.reg
