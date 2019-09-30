from cpu.modules.flag_handler import FlagHandler

class Accumulator():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    # Shifts value (inside given address) 1 bit to the left, with bit 0 set
    # to 0. Result is stored in A
    # Flags: C -> bit 7 from initial value.
    #        N, Z (from result).
    def acc_asl(self):
        oper = self.cpu.a
        res = oper << 1
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarry(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # This instruction shifts the accumulator 1 bit to the right, with
    # the higher bit of the result always being set to 0, and the low
    # bit which is shifted out of the field being stored in the carry flag.
    def acc_lsr(self):
        oper = self.cpu.a
        res = oper >> 1
        c = oper & 1
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(c)
        self.fh.forceNegativeFlag(0)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # The rotate left instruction shifts the accumulator left 1 bit, with
    # the input carry being stored in bit 0 and with the input bit 7 being
    # stored in the carry flag.
    def acc_rol(self):
        oper = self.cpu.a
        leftmost = (oper >> 7) & 1
        res = (oper << 1) + self.cpu.c
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(leftmost)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # The rotate right instruction shifts the accumulator right 1 bit with
    # bit 0 shifted into the carry and carry shifted into bit 7.
    def acc_ror(self):
        oper = self.cpu.a
        rightmost = oper & 1
        res = (self.cpu.c << 7) + (oper >> 1)
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(rightmost)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b
