class PPUMASK:
    EMPHASIZE_BLUE_BIT = 7
    EMPHASIZE_GREEN_BIT = 6
    EMPHASIZE_RED_BIT = 5
    SHOW_SPRITE_BIT = 4
    SHOW_BACKGROUND_BIT = 3
    SHOW_LEFTMOST_SPRITE_BIT = 2
    SHOW_LEFTMOST_BACKGROUND_BIT = 1
    GREYSCALE_BIT = 0

    def __init__(self):
        self.reset()

    def reset(self):
        self.reg = 0

    def write(self, value):
        self.reg = value
