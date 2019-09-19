

class MemoryBus():

    def __init__(self):
        self.ram = [0] * 0x2000         # 0x0    - 0x2000
        self.io = [0] * 0x2020          # 0x2000 - 0x4020
        self.exp_rom = [0] * 0x1FE0     # 0x4020 - 0x6000
        self.sram = [0] * 0x2000        # 0x6000 - 0x8000
        self.prg_rom = [0] * 0x8000     # 0x8000 - 0x10000


    # Select which memory instance is being accessed based on address
    def addr_mux(self, bus_addr):
        if bus_addr < 0x2000:
            return self.ram, bus_addr
        elif bus_addr < 0x4020:
            return self.io, bus_addr - 0x2000
        elif bus_addr < 0x6000:
            return self.exp_rom, bus_addr - 0x4020
        elif bus_addr < 0x8000:
            return self.sram, bus_addr - 0x6000
        else:
            return self.prg_rom, bus_addr - 0x8000

    # Write n bytes starting at start_addr
    # Assumes data is a list with at least n elements
    def write(self, start_addr, data, n = 1):
        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)

            # limit memory value to 1 byte
            mem_instance[addr] = data[i] % 256


    # Read n bytes starting at start_addr
    # Return a list with the n elements read
    def read(self, start_addr, n=1):
        data = [0] * n

        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)
            data[i] = mem_instance[addr]

        return data
