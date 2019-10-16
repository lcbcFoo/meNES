import sys
import argparse
import os
import subprocess
from cpu import *

CLOCK = 1.7897725e6


def read_cartridge(file_name, mem_cpu):
    f = open(file_name, 'rb')
    lines = list(f.readlines())
    data = []
    for i in lines:
        data += i
    data = data[16:]
    mem_cpu.write(0xC000, data, 16384)


def main():
    argParser = argparse.ArgumentParser(
            description='Arguments for meNES emulator.')

    argParser.add_argument('input_file_path',
            help='The path to ROM file that the emulator will run.')
    #argParser.add_argument('-g', '--debug',
    #        help='Run the file on debug mode (prints instructions).')
    #argParser.add_argument('-o', '--output', dest='output_file',
    #        nargs='?', const=(os.getcwd() + "/out.txt"),
    #        help='The path to the output txt file. Default is current directory.')

    args = argParser.parse_args()
    rom = args.input_file_path

    mem_bus = MemoryBus()
    read_cartridge(rom, mem_bus)
    cpu = CPU(mem_bus)

    while True:
        n_cycles = cpu.run()
        # Set a sleep proportional to the number of cycles to simulate
        # 6502 clock rate
        sleep(n_cycles * (1/CLOCK))


if __name__ == '__main__':
    main()
