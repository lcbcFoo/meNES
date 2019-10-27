import pygame
BLACK = pygame.Color(255, 255, 255, 255)
WIDTH = 256*4
HEIGHT = 240*4
SIZE = (WIDTH, HEIGHT)

PALETTES = {
        0x00 : 0x757575,
        0x01 : 0x8f1b27,
        0x02 : 0xab0000,
        0x03 : 0x9f0047,
        0x04 : 0x77008f,
        0x05 : 0x1300ab,
        0x06 : 0x0000a7,
        0x07 : 0x000b7f,
        0x08 : 0x002f43,
        0x09 : 0x004700,
        0x0a : 0x005100,
        0x0b : 0x173f00,
        0x0c : 0x5f3f1b,
        0x0d : 0x000000,
        0x0e : 0x000000,
        0x0f : 0x000000,
        0x10 : 0xbcbcbc,
        0x11 : 0xef7300,
        0x12 : 0xef3b23,
        0x13 : 0xf30083,
        0x14 : 0xbf00bf,
        0x15 : 0x5b00e7,
        0x16 : 0x002bdb,
        0x17 : 0x0f4fcb,
        0x18 : 0x00738b,
        0x19 : 0x009700,
        0x1a : 0x00ab00,
        0x1b : 0x3b9300,
        0x1c : 0x8b8300,
        0x1d : 0x000000,
        0x1e : 0x000000,
        0x1f : 0x000000,
        0x20 : 0xffffff,
        0x21 : 0xffbf3f,
        0x22 : 0xff975f,
        0x23 : 0xfd8ba7,
        0x24 : 0xff7bf7,
        0x25 : 0xb777ff,
        0x26 : 0x6377ff,
        0x27 : 0x3b9bff,
        0x28 : 0x3fbff3,
        0x29 : 0x13d383,
        0x2a : 0x4bdf4f,
        0x2b : 0x98f858,
        0x2c : 0xdbeb00,
        0x2d : 0x000000,
        0x2e : 0x000000,
        0x2f : 0x000000,
        0x30 : 0xffffff,
        0x31 : 0xffe7ab,
        0x32 : 0xffd7c7,
        0x33 : 0xffcbd7,
        0x34 : 0xffc7ff,
        0x35 : 0xdbc7ff,
        0x36 : 0xb3bfff,
        0x37 : 0xabdbff,
        0x38 : 0xa3e7ff,
        0x39 : 0xa3ffe3,
        0x3a : 0xbff3ab,
        0x3b : 0xcfffb3,
        0x3c : 0xf3ff9f,
        0x3d : 0x000000,
        0x3e : 0x000000,
        0x3f : 0x000000
}