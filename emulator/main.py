import sys
import argparse
import os
import subprocess
from cpu import *
from ppu import *
from gui import *
from time import sleep

CLOCK = 1.7897725e6


def read_cartridge(file_name, cpu_mem, ppu_mem):
    f = open(file_name, 'rb')
    lines = list(f.readlines())
    data = []
    for i in lines:
        data += i

    prg_size = data[4] * 0x4000
    chr_size = data[5] * 0x2000

    if prg_size > 0x4000:
        cpu_mem.set_16kb(False)

    cpu_mem.write(0x8000, data[16:], prg_size)

    if chr_size > 0:
        ppu_mem.write(0x0000, data[16+prg_size:], chr_size)



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
    gui = Gui()
    read_cartridge(rom, cpu_mem, ppu_mem)

    ppu = PPU(ppu_mem, gui)
    cpu = CPU(cpu_mem)

    ppu.set_cpu(cpu)
    cpu.set_ppu(ppu)
    cpu_mem.set_ppu(ppu)
    
    dma_counter = 0
    wait_clock = False
    while True:
        # This is the direct memory access
        # When cpu writes N in 0x4014, dma starts, copying 256 bytes
        # from cpu memory starting at 0x100 * N into dma memory (sprites
        # information)
        # During this time, cpu clock is not running, so we count 1 clock
        # passed
        if ppu.dma_on_going:
            read_from_cpu_mem = cpu.mem_bus.read(ppu.dma_page * 0x100 + dma_counter)
            ppu.oam_memory[dma_counter] = read_from_cpu_mem
            dma_counter += 1
            n_cycles = 1

            if dma_counter == 256:
                dma_counter = 0
                ppu.dma_on_going = False

        else:
            n_cycles = cpu.run()

        if ppu.nmi_flag:
            ppu.nmi_flag = False
            cpu.nmi()

        for i in range (0, 3 * n_cycles):
            ppu.run()

        # Set a sleep proportional to the number of cycles to simulate
        # 6502 clock rate
        # TODO: test execution time for this program
        sleep(n_cycles * (1/CLOCK))


if __name__ == '__main__':
    main()
