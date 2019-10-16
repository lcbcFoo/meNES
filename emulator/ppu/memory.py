class PpuMemoryBus():

    def __init__(self):
        self.pattern_tables = [0] * 0x2000      # 0x0    - 0x2000
        self.name_tables = [0] * 0x1F00         # 0x2000 - 0x3F00
        self.palettes = [0] * 0x0100            # 0x3F00 - 0x4000
        # self.mirrors = [0] * 0xC000             # 0x4000 - 0x10000

    # Select which memory instance is being accessed based on address
    def addr_mux(self, bus_addr):
        if bus_addr >= 0 and bus_addr < 0x2000:
            return self.pattern_tables, bus_addr
        elif bus_addr >= 0x2000 and bus_addr < 0x3F00:
            return self.name_tables, (bus_addr - 0x2000) % 0x1000
        elif bus_addr >= 0x3F00 and bus_addr < 0x4000:
            return self.palettes, (bus_addr - 0x3F00) % 0x20
        else:
            return self.addr_mux(bus_addr % 0x4000)

    # Write n bytes starting at start_addr
    # Assumes data is a list with at least n elements
    def write(self, start_addr, data, n=1):
        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)
            mem_instance[addr] = data[i] % 256
        return

    # Read n bytes starting at start_addr
    # Return a list with the n elements read
    def read(self, start_addr, n=1):
        data = [0] * n
        for i in range(0, n):
            mem_instance, addr = self.addr_mux(start_addr + i)
            data[i] = mem_instance[addr]

        if n == 1:
            return data[0]

        return data
