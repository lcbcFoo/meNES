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
        self.OAMADDR = OAMADDR()
        self.OAMDATA = OAMDATA()
        self.OAMDMA = OAMDMA()
        self.PPUADDR = PPUADDR()
        self.PPUCTRL = PPUCTRL()
        self.PPUDATA = PPUDATA()
        self.PPUMASK = PPUMASK()
        self.PPUSCROLL = PPUSCROLL()
        self.PPUSTATUS = PPUSTATUS()

        self.io_registers = {
            0x2000: self.PPUCTRL,
            0x2001: self.PPUMASK,
            0x2002: self.PPUSTATUS,
            0x2003: self.OAMADDR,
            0x2004: self.OAMDATA,
            0x2005: self.PPUSCROLL,
            0x2006: self.PPUADDR,
            0x2007: self.PPUDATA,
            0x4014: self.OAMDMA,
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
