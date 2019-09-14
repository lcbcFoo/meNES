import sys
import argparse
import os
import subprocess
from cpu import *
from memory import *

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
    cpu = CPU(mem_bus)
    cpu.read_cartridge(rom)
    cpu.run()

if __name__ == '__main__':
    main()

