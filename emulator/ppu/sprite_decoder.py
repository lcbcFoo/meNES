from pprint import pprint
import numpy as np

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
        sprite_tiles.append(np.array(new_tyle))

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
    return ans[:256], ans[256:]
