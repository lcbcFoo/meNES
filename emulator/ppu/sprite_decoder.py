import getopt
import os.path
import sys
import png
from pprint import pprint
import numpy as np

CHAR_WIDTH = 8  # character width in pixels
CHAR_HEIGHT = 8  # character height in pixels
BYTES_PER_CHAR = 16  # bytes per character in CHR data
CHARS_PER_ROW = 16  # characters per row in output matrix
TOTAL_ROWS = 32 # amount of tile rows in output matrix

def split_help(array, nrows, ncols):
    """Split a matrix into sub-matrices."""
    print("starting")
    print("Initial dimensions:", array.shape)
    splitted_lines = np.array(np.hsplit(array, ncols))
    if not np.all(splitted_lines == 0):
        print("a")
    print("Splitted lines dimensions:",splitted_lines.shape)
    splitted_cols = np.array(np.hsplit(splitted_lines, TOTAL_ROWS))
    if not np.all(splitted_lines == 0):
        print("b")
    print("Splitted columns dimensions:",splitted_cols.shape)
    return splitted_cols

def split(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def generate_sprite_tiles(lo_byte, hi_byte):
    sprite_tiles = []
    # For each tile
    for i in range(len(lo_byte)):
        new_tyle = []
        # For each tile line
        for j in range(len(lo_byte[i])):
            tile_line = []
            # For each bit in the line
            for k in range(len(lo_byte[i][j])):
                # Get color index and adds it to line
                pallete_color = lo_byte[i][j][k] + 2 * hi_byte[i][j][k]
                tile_line.append(pallete_color)
            # Appends line to tile
            new_tyle.append(tile_line)
        # Appends tile to sprites array
        sprite_tiles.append(new_tyle)

    return sprite_tiles

def int_array_to_bit_matrix(arr):
    bit_matrix = []
    for element in arr:
        bit_str_array = bin(element)[2:].zfill(8)
        bit_array = [1 if digit=='1' else 0 for digit in bit_str_array]
        bit_matrix.append(bit_array)
    # pprint(bit_matrix)
    # print("=====================")
    return bit_matrix

def transform_sprites(pattern_tables):
    '''
    Input: Pattern table array. Each integer is equivalent to 1 byte.
    Output: Array of 8x8 matrices, 0-3 values
    '''
    my_sprites = list(split(pattern_tables, 8))
    my_list = []
    for i in my_sprites:
        l = int_array_to_bit_matrix(i)
        my_list.append(l)
    low, high = my_list[::2], my_list[1::2]
    ans = generate_sprite_tiles(low, high)
    return ans
