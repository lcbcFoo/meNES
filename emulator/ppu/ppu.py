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

PALETTES = {
        0x00 : (0, 0, 0),
        0x01 : (0, 30, 116),
        0x02 : (8, 16, 144),
        0x03 : (48, 0, 136),
        0x04 : (68, 0, 100),
        0x05 : (92, 0, 48),
        0x06 : (84, 4, 0),
        0x07 : (60, 24, 0),
        0x08 : (32, 42, 0),
        0x09 : (8, 58, 0),
        0x0a : (0, 64, 0),
        0x0b : (0, 60, 0),
        0x0c : (0, 50, 60),
        0x0d : (0, 0, 0),
        0x0e : (0, 0, 0),
        0x0f : (0, 0, 0),
        0x10 : (152, 150, 152),
        0x11 : (8, 76, 196),
        0x12 : (48, 50, 236),
        0x13 : (92, 30, 228),
        0x14 : (136, 20, 176),
        0x15 : (160, 20, 100),
        0x16 : (152, 34, 32),
        0x17 : (120, 60, 0),
        0x18 : (84, 90, 0),
        0x19 : (40, 114, 0),
        0x1a : (8, 124, 0),
        0x1b : (0, 118, 40),
        0x1c : (0, 102, 120),
        0x1d : (0, 0, 0),
        0x1e : (0, 0, 0),
        0x1f : (0, 0, 0),
        0x20 : (236, 238, 236),
        0x21 : (76, 154, 236),
        0x22 : (120, 124, 236),
        0x23 : (176, 98, 236),
        0x24 : (228, 84, 236),
        0x25 : (236, 88, 180),
        0x26 : (236, 106, 100),
        0x27 : (212, 136, 32),
        0x28 : (160, 170, 0),
        0x29 : (116, 196, 0),
        0x2a : (76, 208, 32),
        0x2b : (56, 204, 108),
        0x2c : (56, 180, 204),
        0x2d : (60, 60, 60),
        0x2e : (0, 0, 0),
        0x2f : (0, 0, 0),
        0x30 : (236, 238, 236),
        0x31 : (168, 204, 236),
        0x32 : (188, 188, 236),
        0x33 : (212, 178, 236),
        0x34 : (236, 174, 236),
        0x35 : (236, 174, 212),
        0x36 : (236, 180, 176),
        0x37 : (228, 196, 144),
        0x38 : (204, 210, 120),
        0x39 : (180, 222, 120),
        0x3a : (168, 226, 144),
        0x3b : (152, 226, 180),
        0x3c : (160, 214, 228),
        0x3d : (160, 162, 160),
        0x3e : (0, 0, 0),
        0x3f : (0, 0, 0)
}

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
        
        image = np.zeros((240, 256))
        self.background = np.array([[PALETTES[0] for i in j] for j in image])
        self.background_ready = False

    def run(self):
        # We do all work of those 240 scanlines in one cycle, so we just
        # do nothing until 240
        if not self.background_ready and self.ppumask.isBackgroundEnabled():  # Render only the first time
            self.render_background()
            self.background[13:] = self.background[:227]
            self.background[:13] = 0

        # At this point, self.background contains the background where we want
        # to 'stamp' the sprites

        # At scanline 240 we should have our screen ready for next
        # scanline sets NMI. So we stamp sprites here
        if self.ppumask.isSpriteEnabled() and self.cycle == 1:
            self.screen = self.render_sprites()
        # elif self.cycle == 1:
        #     self.screen = self.background

        if self.cycle == 1:
            # At this point, our screen is ready, so we enter vblank state and
            # raise NMI interrupt if bit is set
            self.ppustatus.reg.storeBit(VBLANK_STATUS_BIT, 1)

            if self.ppuctrl.isNMIEnabled():
                self.nmi_flag = True

        # Update cycles and scanline
        self.cycle += 1
        if self.cycle == 700:
            self.cycle = 0
            if self.background_ready:
                # print(self.screen)
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
                        screen[y+iy][x+ix] = PALETTES[cor]

        return screen


    def render_background(self):
        self.background_ready = True
        bg_base = 0x2000
        bg = np.zeros((240, 256))

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
                        bg[base_i + k1][base_j + k2] = sprite[k1][k2]

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
                        addr1 = bg[y1][x1]
                        val1 = map_1[addr1]
                        bg[y1][x1] = val1

                        # Top right
                        y2 = base_y + k1
                        x2 = base_x + k2 + 16
                        addr2 = bg[y2][x2]
                        val2 = map_2[addr2]
                        bg[y2][x2] = val2

                        # Bottom left
                        y3 = base_y + k1 + 16
                        x3 = base_x + k2
                        addr3 = bg[y3][x3]
                        val3 = map_3[addr3]
                        bg[y3][x3] = val3

                        # Bottom right
                        y4 = base_y + k1 + 16
                        x4 = base_x + k2 + 16
                        addr4 = bg[y4][x4]
                        val4 = map_4[addr4]
                        bg[y4][x4] = val4
        self.background = np.array([[PALETTES[i] for i in j] for j in bg])
        print(self.background)
        self.screen = np.copy(self.background)
