class CpuMemoryBus():

    def __init__(self):
        self.set_16kb(True)
        # self._16kb = True
        self.ram = [0] * 0x2000         # 0x0    - 0x2000
        self.io = [0] * 0x2020          # 0x2000 - 0x4020
        self.exp_rom = [0] * 0x1FE0     # 0x4020 - 0x6000
        self.sram = [0] * 0x2000        # 0x6000 - 0x8000
        self.prg_rom = [0] * 0x8000     # 0x8000 - 0x10000

    def set_ppu(self, ppu):
        self.ppu = ppu

    def set_16kb(self, value):
        self._16kb = value

    # Select which memory instance is being accessed based on address
    def addr_mux(self, bus_addr, sys = False):
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
    def write(self, start_addr, data, n = 1, sys = False):
        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)

            curr_addr = addr + 0x2000

            if n == 1:
                curr_data = data % 256
            else:
                curr_data = data[i] % 256

            if mem_instance == self.io and ((curr_addr >= 0x2000 and curr_addr <= 0x2007) or curr_addr == 0x4014):
                self.ppu.register_write(curr_addr, curr_data, sys)

            mem_instance[addr] = curr_data

    # Read n bytes starting at start_addr
    # Return a list with the n elements read
    def read(self, start_addr, n=1, dryrun=False, sys = False):
        data = [0] * n
        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)

            curr_addr = addr + 0x2000
            if (not dryrun) and mem_instance == self.io and ((curr_addr >= 0x2000 and curr_addr <= 0x2007) or curr_addr == 0x4014):
                data[i] = self.ppu.register_read(curr_addr, sys)
            else:
                data[i] = mem_instance[addr]

        if n == 1:
            return data[0]

        return data
