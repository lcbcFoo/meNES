import sys
import copy
from pprint import pprint
import copy
import numpy as np

from ppu.registers.oam_address import *
from ppu.registers.oam_data import *
from ppu.registers.oam_dma import *
from ppu.registers.ppu_address import *
from ppu.registers.ppu_control import *
from ppu.registers.ppu_data import *
from ppu.registers.ppu_mask import *
from ppu.registers.ppu_scroll import *
from ppu.registers.ppu_status import *
from ppu.register import Register8Bit, Register16Bit
from ppu.sprite_decoder import *


class PPU:

    def __init__(self, mem_bus, gui):
        self.set_memory(mem_bus)
        self.gui = gui

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

        # ppu cycle and scanline counter
        self.cycle = 0;
        self.scanline = -1

        # Flag for on going DMA
        self.dma_on_going = False

        # OAM memory region
        self.oam_memory = [0] * 256

        # DMA page used in DMA operation
        self.dma_page = 0

        # NMI flag
        self.nmi_flag = False

        self.background = np.zeros((240,256))

        self.background_ready = False

    def run(self):
        # We do all work of those 240 scanlines in one cycle, so we just
        # do nothing until 240
        if not self.background_ready:  # Render only the first time
            self.render_background()
            self.background[13:] = self.background[:227]
            self.background[:13] = 0

        # At this point, self.background contains the background where we want
        # to 'stamp' the sprites

        # At scanline 240 we should have our screen ready for next
        # scanline sets NMI. So we stamp sprites here
        if self.cycle == 1:
            self.screen = self.render_sprites()
        # At this point, our screen is ready, so we enter vblank state and
        # raise NMI interrupt if bit is set
            self.ppustatus.reg.storeBit(VBLANK_STATUS_BIT, 1)

            if self.ppuctrl.isNMIEnabled():
                self.nmi_flag = True

        # Update cycles and scanline
        self.cycle += 1
        if self.cycle == 700:
            self.cycle = 0
            self.gui.draw_screen(self.screen)


    def register_write(self, addr, value, sys = False):
        self.io_registers[addr].write(value, sys)

    def register_read(self, addr, sys = False):
        return self.io_registers[addr].read(sys)

    def render_sprites(self):
        screen = np.copy(self.background)
        for i in range(64):
            base_addr = i*4
            y = self.oam_memory[base_addr]
            sprite_num = self.oam_memory[base_addr+1]
            attr = self.oam_memory[base_addr+2]
            x = self.oam_memory[base_addr+3]

            pal_1 = attr & 0b00000011
            pal_2 = (attr & 0b00001100) >> 2
            pal_3 = (attr & 0b00110000) >> 4
            pal_4 = (attr & 0b11000000) >> 6

            map1 = dict([(k, v & 0x3f) for k, v in zip(range(1, 4),
                self.mem_bus.read(0x3f10 + pal_1 * 4 + 1, 3))])
            map1[0] = 0x00

            for iy in range(8):
                for ix in range(8):
                    cor = map1[self.sprite_table[sprite_num][iy][ix]]
                    if cor != 0:
                        screen[y+iy][x+ix] = cor

        return screen


    def render_background(self):
        self.background_ready = True
        bg_base = 0x2000

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

        # Read the 64 bytes that tell us which palette to use to each sprite
        for i in range(30, 32):
            for j in range(0, 32):
                # read the byte
                addr = bg_base + (i * 32) + j
                byte = self.mem_bus.read(addr)

                # interpret its bits to look for palette ID
                pal_1 = byte & 0b00000011
                pal_2 = (byte & 0b00001100) >> 2
                pal_3 = (byte & 0b00110000) >> 4
                pal_4 = (byte & 0b11000000) >> 6

                # each attribute separates a tile into 4 2x2 quadrants
                # pal_1 is for the top left, pal_2 for top right,
                # pal_3 bot left and pal_4 bot right

                # palettes are located at address 0x3f00-3f1d
                # 0x3f00 is the background color
                # 0x3f01 - 0x3f04 is the palette ID 1 and so on
                # then the palette ID is basically an offset to add to the
                # pixel bits (0, 1, 2, 3) to search for its matching color

                # Compose the mapping number:color for each palette
                # In all maps, value 0 mirrors background color, which
                # is located at 0x3f00
                bg_color = self.mem_bus.read(0x3f00)
                map_1 = dict([(k, v & 0x3f) for k, v in zip(range(1, 4),
                    self.mem_bus.read(0x3f00 + pal_1 * 4 + 1, 3))])
                map_1[0] = bg_color

                map_2 = dict([(k, v & 0x3f) for k, v in zip(range(1, 4),
                    self.mem_bus.read(0x3f00 + pal_2 * 4 + 1, 3))])
                map_2[0] = bg_color

                map_3 = dict([(k, v & 0x3f) for k, v in zip(range(1, 4),
                    self.mem_bus.read(0x3f00 + pal_3 * 4 + 1, 3))])
                map_3[0] = bg_color

                map_4 = dict([(k, v & 0x3f) for k, v in zip(range(1, 4),
                    self.mem_bus.read(0x3f00 + pal_4 * 4 + 1, 3))])
                map_4[0] = bg_color


                # Now we have each map for each quadrant of the 32x32 tile
                # Meaning, 4 16x16 squares
                #     16 16
                #      _ _
                # 16  |_|_| 16
                # 16  |_|_| 16
                #     16 16

                # We define the base address (top left) of the tile we
                # are coloring with this attibute
                base_y = (32 * (j // 8)) + 128 * (i - 30 )
                base_x = (j * 32) % 256

                # This represents the end of the screen -> finish
                if base_y >= 224:
                    break

                # Now, we map the correspondig map for each quadrant
                for k1 in range(0, 16):
                    for k2 in range(0, 16):

                        # Top left
                        y1 = base_y + k1
                        x1 = base_x + k2
                        addr1 = self.background[y1][x1]
                        val1 = map_1[addr1]
                        self.background[y1][x1] = val1

                        # Top right
                        y2 = base_y + k1
                        x2 = base_x + k2 + 16
                        addr2 = self.background[y2][x2]
                        val2 = map_2[addr2]
                        self.background[y2][x2] = val2

                        # Bottom left
                        y3 = base_y + k1 + 16
                        x3 = base_x + k2
                        addr3 = self.background[y3][x3]
                        val3 = map_3[addr3]
                        self.background[y3][x3] = val3

                        # Bottom right
                        y4 = base_y + k1 + 16
                        x4 = base_x + k2 + 16
                        addr4 = self.background[y4][x4]
                        val4 = map_4[addr4]
                        self.background[y4][x4] = val4
