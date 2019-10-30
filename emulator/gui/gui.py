import sys
import pygame
import time
import numpy as np

from gui.constants import *

class Gui():
    def __init__(self):
        # Initialize pygame
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print("There was a problem initializing pygame")
            sys.exit(-1)

        # Screen
        self.screen = pygame.display.set_mode(SIZE)

    def draw_screen(self, image):
        # Redraw screen
        image = image.transpose()

        # Convert NES palette to RGB color
        image = np.array([[PALETTES[i] for i in j] for j in image])

        # Make a surface in pygame based on image and show it
        surface = pygame.surfarray.make_surface(image)
        im = pygame.transform.scale(surface, SIZE)
        self.screen.blit(im, pygame.Rect((0, 0), SIZE))
        pygame.display.flip()


if __name__ == "__main__":
    gui = Gui()
    i = 1
    for k in range(0, 120):
        i = 1 + ((i + 1) % 60)
        gui.draw_screen([[i, 0x40 - i], [0x40 - i, i]])
        gui.draw_screen([[0x40 - i, i], [i,0x40 - i]])
