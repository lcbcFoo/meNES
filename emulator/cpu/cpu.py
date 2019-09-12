import sys
from collections import namedtuple
from mem import *
from modules.absolute import *
from modules.opcodes import *

class CPU:
    
    def __init__(self, mem):
        # TODO: change to mem[0xFFA0]
        self.pc = 0xC000
        self.mem = mem
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

        while True:
            # TODO: change to read mem[pc]
            # opcode = 0x00
            abs = Absolute(self, self.mem)
            opcode = mem.data[0]
            op = absolute_opcodes[opcode].method
            op(abs)
            # TODO: search for opcode in dictionary and execute instruction
            exit(0)



    def read_cartridge(self, lines, output_file):
        # Writes txt file if output_file is set
        if output_file is not None:
            print("Writing file:", output_file)
            with open(output_file, 'w') as f:
                for element in lines:
                    f.write("%s\n" % element)
        else:
            print("Printing lines on terminal:")
            for element in lines:
                print(element)


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

if __name__ == "__main__":
    mem = Mem()
    cpu = CPU(mem)
    cpu.run()
