import sys
import argparse
import os
import subprocess
from cpu import *
from ppu import *
from time import sleep

CLOCK = 1.7897725e6


def read_cartridge(file_name, cpu_mem, ppu_mem):
    f = open(file_name, 'rb')
    lines = list(f.readlines())
    data = []
    for i in lines:
        data += i
    data = data[16:]
    cpu_mem.write(0xC000, data, 16384)


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

    cpu_mem = CpuMemoryBus()
    ppu_mem = PpuMemoryBus()

    read_cartridge(rom, cpu_mem, ppu_mem)
    ppu = PPU(ppu_mem)
    cpu = CPU(cpu_mem, ppu)


    while True:
        n_cycles = cpu.run()

        for i in range (0, n_cycles):
            ppu.run()

        # Set a sleep proportional to the number of cycles to simulate
        # 6502 clock rate
        # TODO: test execution time for this program
        sleep(n_cycles * (1/CLOCK))


if __name__ == '__main__':
    main()
