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
from ppu.register import Register8Bit, Register16Bit
# from ppu.sprite_decoder import *

class PPU:

    def __init__(self, mem_bus):
        self.set_memory(mem_bus)

        # io registers
        self.oamaddr = OAMADDR(self, Register8Bit())
        self.oamdata = OAMDATA(self, Register8Bit())
        self.oamdma = OAMDMA(self, Register8Bit())
        self.ppuaddr = PPUADDR(self, Register16Bit())
        self.ppuctrl = PPUCTRL(self, Register8Bit())
        self.ppudata = PPUDATA(self, Register8Bit())
        self.ppumask = PPUMASK(self, Register8Bit())
        self.ppuscroll = PPUSCROLL(self, Register16Bit())
        self.ppustatus = PPUSTATUS(self, Register8Bit())

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

        # Inside shift-registers
        self.nameTableRegister = Register8Bit()
        self.attributeTableLowRegister = Register16Bit()
        self.attributeTableHighRegister = Register16Bit()
        self.patternTableLowRegister = Register16Bit()
        self.patternTableHighRegister = Register16Bit()

        # inside latches
        self.nameTableLatch = 0
        self.attributeTableLowLatch = 0
        self.attributeTableHighLatch = 0
        self.patternTableLowLatch = 0
        self.patternTableHighLatch = 0

        # Building sprites matrix
        # self.sprites = decode_sprites(self.mem_bus.pattern_tables)

        self.reset()

    def set_memory(self, mem_bus):
        self.mem_bus = mem_bus

    def set_cpu(self, cpu):
        self.cpu = cpu

    def reset(self):
        for key in self.io_registers:
            self.io_registers[key].reset()


    def run(self):
        self.render_pixel()
        self.shift_registers()
        self.fetch()
        self.evaluate_sprites()
        self.update_flags()
        self.count_up_scroll_counters()
        self.count_up_cycle()
        pass

    def register_write(self, addr, value):
        self.io_registers[addr].write(value)

    def register_read(self, addr):
        return self.io_registers[addr].read()

    # Get BG and sprites values and prints and put it on the screen.
    def render_pixel(self):
        pass

    # Updates values on shift registers (pixels infos).
    def shift_registers(self):
        pass

    # According to the cycle, fetches value on VRAM and puts on shift registers.
    def fetch(self):
        pass

    # Prepares sprite infos for next scanline.
    def evaluate_sprites(self):
        pass

    # Sets/Clears VBlank, ZeroHit and Overflow flags according to scanline.
    def update_flags(self):
        pass

    # Honestly, ???
    def count_up_scroll_counters(self):
        pass

    # Increments cycle --> maybe this will not be used here.
    def count_up_cycle(self):
        pass
