import sys
from collections import namedtuple
from ..memory import Memory
from .modules.absolute import Absolute
from .modules.flag_handler import FlagHandler
from .modules.opcodes import *

class CPU:
    def __init__(self, bus):
        self.mem_bus = bus
        self.flag_handler = FlagHandler(self)

    def reset(self):
        self.pc = self.mem_bus.read(0xFFA0)

        # Registers
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00

        # Stack pointer
        self.sp = 0x00

        # Control flags
        self.n = 0
        self.v = 0
        self.b = 0
        self.d = 0
        self.i = 0
        self.z = 0
        self.c = 0

    def run(self):
        self.reset()

        while True:
            # TODO: change to read mem[pc]
            # opcode = 0x00
            # abs = Absolute(self, self.mem)
            # opcode = self.mem_bus.data[0]
            # op = absolute_opcodes[opcode].method
            # op(abs)
            # TODO: search for opcode in dictionary and execute instruction
            exit(0)



    def read_cartridge(self, file_name):
        f = open(file_name, 'rb')
        lines = [i for i in f.readlines()][0]
        lines = lines[16:]
        self.mem_bus.write(0xC000, lines, len(lines))

    def dump_mem(self):
        o = open('mem_dump.txt', 'w')
        data = self.mem_bus.read(0, 0x10000)
        o.write('\n'.join([hex(i) for i in data]))

    # Log
    def log(self):
        s = '| pc = ' + format(self.pc, '#06x')
        s += ' | a = ' + format(self.a, '#04x')
        s += ' | x = ' + format(self.x, '#04x')
        s += ' | y = ' + format(self.y, '#04x')
        s += ' | sp = ' + format(self.a, '#06x')
        s += ' | p[NV-BDIZC] = ' + str(self.n) + str(self.v) + str(0) + str(self.b) 
        s += str(self.d) + str(self.i) + str(self.z) + str(self.c) + ' |'
        return s

    def logls(self, addr, val):
        s = self.log()
        s += ' MEM[' + format(addr, '#06x') + '] = ' + format(val, '#04x') + ' |'
        return s

    def print_log(self, ls=False, addr=0, val=0):
        if ls:
            print(self.logls(addr, val))
        else:
            print(self.log())
