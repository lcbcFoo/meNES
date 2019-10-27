import sys
import copy
from pprint import pprint

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
from ppu.sprite_decoder import *


class PPU:

    def __init__(self, mem_bus, gui):
        self.set_memory(mem_bus)
        self.gui = gui

        # ppu cycle and scanline counter
        self.cycle = 0;
        self.scanline = 0

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
        self.sprite_table = transform_sprites(self.mem_bus.pattern_tables)

        self.reset()

    def set_memory(self, mem_bus):
        self.mem_bus = mem_bus

    def set_cpu(self, cpu):
        self.cpu = cpu

    def reset(self):
        for key in self.io_registers:
            self.io_registers[key].reset()
        #self.render_background()


    def run(self):
        self.render_pixel()
        self.shift_registers()
        self.fetch()
        self.evaluate_sprites()
        self.update_flags()
        self.count_up_scroll_counters()
        self.count_up_cycle()
        pass

    def register_write(self, addr, value, sys = False):
        self.io_registers[addr].write(value, sys)

    def register_read(self, addr, sys = False):
        return self.io_registers[addr].read(sys)

    def render_background(self):
        # Undestand this part
        # Load the current background tile pattern and attributes into the "shifter"
        #LoadBackgroundShifters();

        # Fetch background tiles
        # "(vram_addr.reg & 0x0FFF)" : Mask to 12 bits that are relevant
        # "| 0x2000"                 : Offset into nametable space on PPU address bus
        bg_base = 0x2000
        #addr = bg_base | (vram_addr.reg & 0x0FFF));

        self.background = [[0]*256 for i in range(0,240)]

        # Background name table is composed by 32 * 32 bytes
        # Last 2 rows of bytes are attributes for color, we will look later

        # Read each byte of the 30 x 32 bytes that are not attribute
        # Each of these bytes is an ID to be looked on the pattern table (sprites)
        for i in range(0, 30):
            for j in range(0, 32):
                addr = bg_base + (i * 32) + j
                sprite = self.sprite_table[self.mem_bus.read(addr)]
                for k1 in range(0, 8):
                    for k2 in range(0, 8):
                        base_i = 8 * i
                        base_j = 8 * j
                        self.background[base_i + k1][base_j + k2] = sprite[k1][k2]
        print(self.mem_bus.read(0x23c0, 64))
        
        # Read the 64 bytes that tell us which palette to use to each sprite
        for i in range(30, 32):
            for j in range(0, 32):
                # read the byte
                addr = bg_base + (i * 32) + j
                byte = self.mem_bus.read(addr)
                #print(hex(addr))
                #print(bin(byte))

                # interpret its bits to look for palette ID
                pal_1 = byte & 0b00000011
                pal_2 = (byte & 0b00001100) >> 2
                pal_3 = (byte & 0b00110000) >> 4
                pal_4 = (byte & 0b11000000) >> 6

                # each attribute separates a tile into 4 2x2 quadrants
                # pal_1 is for the top left, pal_@ for top right,
                # pal_3 bot left and pal_4 bot right

                # palettes are located at address 0x3f00-3f1d
                # 0x3f00 is the background color
                # 0x3f01 - 0x3f04 is the palette ID 1 and so on
                # then the palette ID is basically an offset to add to the
                # pixel bits (0, 1, 2, 3) to search for its matching color
                
                # Compose the mapping number:color for each palette
                print(self.mem_bus.read(0x3f00, 16))
                print(pal_1,pal_2,pal_3, pal_4)
                map_1 = dict([(k, v) for k, v in zip(range(0, 4),
                    self.mem_bus.read(0x3f00 + pal_1 * 4, 4))])
                map_2 = dict([(k, v) for k, v in zip(range(0, 4),
                    self.mem_bus.read(0x3f00 + pal_2 * 4, 4))])
                map_3 = dict([(k, v) for k, v in zip(range(0, 4),
                    self.mem_bus.read(0x3f00 + pal_3 * 4, 4))])
                map_4 = dict([(k, v) for k, v in zip(range(0, 4),
                    self.mem_bus.read(0x3f00 + pal_4 * 4, 4))])

                # print(map_1)
                # print(map_2)
                # print(map_3)
                # print(map_4)

                base_y = 8 * ((j // 32) + (i - 30))
                base_x = j * 8
                #print(base_y,base_x)
                for k1 in range(0, 4):
                    for k2 in range(0, 4):
                        y1 = base_y + k1
                        x1 = base_x + k2
                        addr1 = self.background[y1][x1]
                        val1 = map_1[addr1]
                        self.background[y1][x1] = val1

                        y2 = base_y + k1
                        x2 = base_x + k2 + 4
                        addr2 = self.background[y2][x2]
                        val2 = map_2[addr2]
                        self.background[y2][x2] = val2
                        
                        y3 = base_y + k1 + 4
                        x3 = base_x + k2
                        addr3 = self.background[y3][x3]
                        val3 = map_3[addr3]
                        self.background[y3][x3] = val3
                        
                        y4 = base_y + k1 + 4
                        x4 = base_x + k2 + 4
                        addr4 = self.background[y4][x4]
                        val4 = map_4[addr4]
                        self.background[y4][x4] = val4

        self.gui.draw_screen(self.background)
        pass
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
