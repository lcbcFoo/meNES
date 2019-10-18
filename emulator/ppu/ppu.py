import sys

from ppu.registers.oam_address import OAMADDR
from ppu.registers.oam_data import OAMDATA
from ppu.registers.oam_dma import OAMDMA
from ppu.registers.ppu_address import PPUADDR
from ppu.registers.ppu_control import PPUCTRL
from ppu.registers.ppu_data import PPUDATA
from ppu.registers.ppu_mask import PPUMASK
from ppu.registers.ppu_scroll import PPUSCROLL
from ppu.registers.ppu_status import PPUSTATUS

class PPU:

    def __init__(self, mem_bus):
        self.mem_bus = mem_bus
        self.oamaddr = OAMADDR(self)
        self.oamdata = OAMDATA(self)
        self.oamdma = OAMDMA(self)
        self.ppuaddr = PPUADDR(self)
        self.ppuctrl = PPUCTRL(self)
        self.ppudata = PPUDATA(self)
        self.ppumask = PPUMASK(self)
        self.ppuscroll = PPUSCROLL(self)
        self.ppustatus = PPUSTATUS(self)

        self.io_registers = {
            0x2000: self.ppuctrl,
            0x2001: self.ppumask,
            0x2002: self.ppustatus,
            0x2003: self.oamaddr,
            0x2004: self.oamdata,
            0x2005: self.ppuscroll,
            0x2006: self.ppuaddr,
            0x2007: self.ppudata,
            0x4014: self.oamdma,
        }

        self.reset()

    def reset(self):
        # for key in self.io_registers:
        #     self.io_registers[key].reset()
        pass


    def run(self):
        pass

    def register_write(self, addr, value):
        self.io_registers[addr].write(value)

    def register_read(self, addr):
        return self.io_registers[addr].read()
