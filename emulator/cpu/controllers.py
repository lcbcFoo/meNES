import pygame

class Controller:

    def __init__(self):
        self.state = [0] * 2

    def set_state(self, index, val):
        self.state[index] = val

    def get_state(self, index):
        val = self.state[index]
        self.set_state(index, (val << 1) % 256)
        return val

    def get_ctrl2_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_o]:                    # A
            data = 0x80
        elif keys[pygame.K_p]:                  # B
            data = 0x40
        elif keys[pygame.K_l]:                  # select
            data = 0x20
        elif keys[pygame.K_RETURN]:             # start
            data = 0x10
        elif keys[pygame.K_UP]:                 # up
            data = 0x08
        elif keys[pygame.K_DOWN]:               # down
            data = 0x04
        elif keys[pygame.K_LEFT]:               # left
            data = 0x02
        elif keys[pygame.K_RIGHT]:              # right
            data = 0x01
        else:
            data = 0x00

        pygame.event.pump()
        return data


    def get_ctrl1_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_v]:                    # A
            data = 0x80
        elif keys[pygame.K_c]:                  # B
            data = 0x40
        elif keys[pygame.K_x]:                  # select
            data = 0x20
        elif keys[pygame.K_SPACE]:              # start
            data = 0x10
        elif keys[pygame.K_w]:                  # up
            data = 0x08
        elif keys[pygame.K_s]:                  # down
            data = 0x04
        elif keys[pygame.K_a]:                  # left
            data = 0x02
        elif keys[pygame.K_d]:                  # right
            data = 0x01
        else:
            data = 0x00

        pygame.event.pump()
        return data
