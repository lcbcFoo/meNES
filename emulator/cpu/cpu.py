import sys
from collections import namedtuple
from array import array

from cpu.modules.opcodes import opcodes_dict
from cpu.modules.decoder import Decoder

from cpu.modules.zero_page import ZeroPage
from cpu.modules.absolute import Absolute
from cpu.modules.immediate import Immediate
from cpu.modules.implied import Implied
from cpu.modules.indirect import Indirect
from cpu.modules.relative import Relative
from cpu.modules.accumulator import Accumulator
from cpu.modules.flag_handler import FlagHandler

class CPU:

    def __init__(self, mem_bus):
        # Create instances of the classes
        # I did it separetely because I dont know if this can be done directly
        # inside types_dict. But change it later if it can.
        self.set_memory(mem_bus)
        self.set_decoder()
        self.set_flag_handler()

        self.imm = Immediate(self, self.mem_bus, self.decoder)
        self.zp = ZeroPage(self, self.mem_bus, self.decoder)
        self.abs = Absolute(self, self.mem_bus, self.decoder)
        self.ind = Indirect(self, self.mem_bus, self.decoder)
        self.impl = Implied(self, self.mem_bus, self.decoder)
        self.rel = Relative(self, self.mem_bus, self.decoder)
        self.acc = Accumulator(self, self.mem_bus, self.decoder)

        self.types_dict = {
            'immediate': self.imm,
            'zeropage': self.zp,
            'zeropage_x': self.zp,
            'zeropage_y': self.zp,
            'absolute': self.abs,
            'absolute_x': self.abs,
            'absolute_y': self.abs,
            'indirect': self.ind,
            'indirect_x': self.ind,
            'indirect_y': self.ind,
            'implied': self.impl,
            'relative': self.rel,
            'accumulator': self.acc,
        }

        self.reset()

    def set_memory(self, mem_bus):
        self.mem_bus = mem_bus

    def set_decoder(self):
        self.decoder = Decoder(self, self.mem_bus)

    def set_flag_handler(self):
        self.flag_handler = FlagHandler(self)

    def set_ppu(self, ppu):
        self.ppu = ppu

    def reset(self):

        # Resets PC to address specified at position 0xFFFC
        self.pc = self.mem_bus.read(0xFFFC)
        self.pc += self.mem_bus.read(0xFFFD) << 8

        # Registers
        self.a = 0x00
        self.x = 0x00
        self.y = 0x00

        # Stack pointer
        #0100-01FF   RAM used for stack processing and for absolute addressing.
        self.sp = 0xFD

        # Control flags
        self.n = 0
        self.v = 0
        self.b = 1
        self.d = 0
        self.i = 1
        self.z = 0
        self.c = 0

        # Flag to indicate that PC has to be updated, it will be false if
        # a branch or jump were performed
        self.update_pc = True

    def run(self):
        self.update_pc = True
        opcode = self.mem_bus.read(self.pc)
        instr_type = opcodes_dict[opcode].type
        self.decoder.update(instr_type)   #read instructions from memory
        # opcode = self.decoder.opcode  # get instruction opcode

        if opcode == 0:
            exit(0)

        # get instance for the correct class
        op_instance = self.types_dict[opcodes_dict[opcode].type]
        # call method associated with opcode
        address = opcodes_dict[opcode].method(op_instance)

        # Update pc if no branch/jump occured
        if self.update_pc:
            self.pc += opcodes_dict[opcode].bytes

        # Show log for this instruction
        # if(address != None):
        #     val = self.mem_bus.read(address, dryrun=True)
        #     self.print_log(True, address, val)
        # else:
        #     self.print_log()

        return opcodes_dict[opcode].cycles

    def nmi(self):
        next_pc = self.pc
        PCH = (next_pc >> 8) & 255
        self.push_stack(PCH)
        PCL = next_pc & 255
        self.push_stack(PCL)
        self.push_stack(self.create_status_reg())
        self.pc = self.mem_bus.read(0xFFFA)
        self.pc += self.mem_bus.read(0xFFFB) << 8
        self.run()

    def push_stack(self, value):
        stack_addr = 0x0100 + self.sp
        self.mem_bus.write(stack_addr, value)
        self.sp -= 1

    def pop_stack(self):
        self.sp += 1
        stack_addr = 0x0100 + self.sp
        return self.mem_bus.read(stack_addr)

    def create_status_reg(self):
        status_reg = 0
        status_reg += (self.n << 7)
        status_reg += (self.v << 6)
        status_reg += (0x01 << 5)
        status_reg += (self.b << 4)
        status_reg += (self.d << 3)
        status_reg += (self.i << 2)
        status_reg += (self.z << 1)
        status_reg += self.c
        return status_reg

    def restore_status_reg(self, status_reg):
        self.c = status_reg & (0x01 << 0 )
        self.z = (status_reg & (0x01 << 1 ))>>1
        self.i = (status_reg & (0x01 << 2 ))>>2
        self.d = (status_reg & (0x01 << 3 ))>>3
        self.b = (status_reg & (0x01 << 4 ))>>4
        self.v = (status_reg & (0x01 << 6 ))>>6
        self.n = (status_reg & (0x01 << 7 ))>>7


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
        s += ' | sp = ' + format(self.sp+0x0100, '#06x')
        s += ' | p[NV-BDIZC] = ' + str(self.n) + str(self.v) + str(1) + str(self.b)
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
