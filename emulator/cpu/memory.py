import pygame

class CpuMemoryBus():

    def __init__(self):
        self.set_16kb(True)

        self.ram = [0] * 0x2000         # 0x0    - 0x2000
        self.io = [0] * 0x2020          # 0x2000 - 0x4020
        self.exp_rom = [0] * 0x1FE0     # 0x4020 - 0x6000
        self.sram = [0] * 0x2000        # 0x6000 - 0x8000
        self.prg_rom = [0] * 0x8000     # 0x8000 - 0x10000

        self.controller_state = [0] * 2

    def set_ppu(self, ppu):
        self.ppu = ppu

    def set_16kb(self, value):
        self._16kb = value

    # Select which memory instance is being accessed based on address
    def addr_mux(self, bus_addr, sys=False):
        if bus_addr < 0x2000:
            return self.ram, bus_addr % 0x0800
        elif bus_addr < 0x4000:
            return self.io, (bus_addr - 0x2000) % 0x0008
        elif bus_addr < 0x4020:
            return self.io, bus_addr - 0x2000
        elif bus_addr < 0x6000:
            return self.exp_rom, bus_addr - 0x4020
        elif bus_addr < 0x8000:
            return self.sram, bus_addr - 0x6000
        elif bus_addr < 0x10000:
            if self._16kb:
                return self.prg_rom, (bus_addr - 0x8000) % 0x4000
            else:
                return self.prg_rom, bus_addr - 0x8000
        else:
            return 0xFFFF

    # Write n bytes starting at start_addr
    # Assumes data is a list with at least n elements
    def write(self, start_addr, data, n=1, sys=False):
        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)

            curr_addr = addr + 0x2000

            if n == 1:
                curr_data = data % 256
            else:
                curr_data = data[i] % 256

            if mem_instance == self.io and ((curr_addr >= 0x2000 and curr_addr <= 0x2007) or curr_addr == 0x4014):
                self.ppu.register_write(curr_addr, curr_data, sys)
            elif mem_instance == self.io:
                if curr_addr == 0x4016:
                    curr_data = self.get_ctrl1_input()
                    self.controller_state[0] = curr_data
                elif curr_addr == 0x4017:
                    curr_data = self.get_ctrl2_input()
                    self.controller_state[1] = curr_data

            mem_instance[addr] = curr_data

    # Read n bytes starting at start_addr
    # Return a list with the n elements read
    def read(self, start_addr, n=1, dryrun=False, sys=False):
        data = [0] * n
        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)

            curr_addr = addr + 0x2000
            if (not dryrun) and mem_instance == self.io and ((curr_addr >= 0x2000 and curr_addr <= 0x2007) or curr_addr == 0x4014):
                data[i] = self.ppu.register_read(curr_addr, sys)
            elif mem_instance == self.io and (curr_addr == 0x4016 or curr_addr == 0x4017):
                data[i] = (self.controller_state[curr_addr % 2] & 0x80) >> 7
                val_update = (self.controller_state[curr_addr % 2] << 1) % 256
                if (not dryrun):
                    self.controller_state[curr_addr % 2] = val_update
            else:
                data[i] = mem_instance[addr]

        if n == 1:
            return data[0]

        return data

    def get_ctrl1_input(self):
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


    def get_ctrl2_input(self):
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
