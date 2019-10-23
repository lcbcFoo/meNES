import getopt
import os.path
import sys
import png
from pprint import pprint
import numpy as np

CHAR_WIDTH = 8  # character width in pixels
CHAR_HEIGHT = 8  # character height in pixels
BYTES_PER_CHAR = 16  # bytes per character in CHR data
CHARS_PER_ROW = 16  # characters per row in output image
SPRITE_SIZE = 8192 # Standard sprite CHR file size in bytes
DEFAULT_PALETTE = ("000000", "555555", "aaaaaa", "ffffff")

def split_help(array, nrows, ncols):
    """Split a matrix into sub-matrices."""
    
    print("Initial dimensions:", array.shape)
    splitted_lines = np.array(np.hsplit(array, ncols))

    print("Splitted lines dimensions:",splitted_lines.shape)
    splitted_cols = np.array(np.hsplit(splitted_lines, 32))
    print("Splitted columns dimensions:",splitted_cols.shape)
    pprint(splitted_cols[0][0])
    return splitted_cols

def generate_character_rows(source):
    """Yield one character row of CHR data per call."""

    size = source.seek(0, 2)
    source.seek(0)
    while source.tell() < size:
        yield source.read(CHARS_PER_ROW * BYTES_PER_CHAR)

def decode_character_slice(loByte, hiByte):
    """Decode one pixel row of one character."""

    # the data is planar; decode least significant bits first
    pixels = []
    for x in range(CHAR_WIDTH):
        pixels.append((loByte & 1) | ((hiByte & 1) << 1))
        loByte >>= 1
        hiByte >>= 1
    # return the pixels in correct order
    return reversed(pixels)

def generate_pixel_rows(source):
    """Generate pixel rows from the CHR data file."""

    pixels = []  # the pixel row to yield
    for chrData in generate_character_rows(source):  # character rows
        for pixelY in range(CHAR_HEIGHT):  # pixel rows
            pixels.clear()
            for charX in range(CHARS_PER_ROW):  # characters
                # get low and high byte of current character slice
                chrDataIndex = charX * BYTES_PER_CHAR + pixelY
                loByte = chrData[chrDataIndex]
                hiByte = chrData[chrDataIndex + 8]
                # decode slice and add to pixel row
                pixels.extend(decode_character_slice(loByte, hiByte))
            yield pixels

def decode_sprites(chr_file):
    '''
    Input: CHR sprite file
    Output: matrix of 8x8 matrices, 0-3 values

    128 pixels per line
    256 lines
    Each tile is 8x8
    Output is a 32 rows x 16 cols matrix, each element a 8x8 tile
    '''

    with open(chr_file, "rb") as source:
        targetRows = generate_pixel_rows(source)
        targetArray = np.array(list(targetRows))

    out = split_help(targetArray, 32, 16)

    return out