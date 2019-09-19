import sys
from collections import namedtuple

from cpu.modules.opcodes import opcodes_dict
from cpu.modules.decoder import Decoder

from cpu.modules.zero_page import ZeroPage
from cpu.modules.absolute import Absolute
from cpu.modules.immediate import Immediate
from cpu.modules.implied import Implied

class CPU:

    def __init__(self, bus):
        self.mem_bus = bus
        self.decoder = Decoder(self, self.mem_bus)

        # Create instances of the classes
        # I did it separetely because I dont know if this can be done directly
        # inside types_dict. But change it later if it can.
        self.imm = Immediate(self, self.mem_bus, self.decoder)
        self.zp = ZeroPage(self, self.mem_bus, self.decoder)
        self.abs = Absolute(self, self.mem_bus, self.decoder)
        # self.idr = Indirect(self, self.mem_bus, self.decoder)
        # self.impl = Implied(self, self.mem_bus, self.decoder)
        # self.rel = Relative(self, self.mem_bus, self.decoder)
        # self.acc = Accumulator(self, self.mem_bus, self.decoder)

        self.types_dict = {
            'immediate': self.imm,
            'zeropage': self.zp,
            'absolute': self.abs,
            # 'indirect': self.idr,
            # 'implied': self.impl,
            # 'relative': self.rel,
            # 'accumulator': self.acc,
        }

    def reset(self):

        # Resets PC to address specified at position 0xFFFC
        self.pc = self.mem_bus.read(0xFFFC)
        self.pc += self.mem_bus.read(0xFFFD) << 8

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

        # TODO: change while control.
        while True:
            self.decoder.update()   #read instructions from memory
            opcode = '65'  # replace line just for testing
            # opcode = self.decoder.opcode  # get instruction opcode
            # get instance for the correct class
            op_instance = self.types_dict[opcodes_dict[opcode].type]
            # call method associated with opcode
            opcodes_dict[opcode].method(op_instance)
            # update pc
            self.pc += opcodes_dict[opcode].bytes  #TODO: deal with jumps.
            # dont know what else needs to be done :D
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
