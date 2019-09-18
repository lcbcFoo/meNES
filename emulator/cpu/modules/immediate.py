from flag_handler import *

class Immediate(self):
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    def imd_adc(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        carry = self.cpu.c
        result = reg_a + immediate + carry
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.SetCarry(result)
        self.fh.SetOverflow(reg_a, immediate, result_8b)
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_and(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a & immediate
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_cmp(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a - immediate
        result_8b = self.fh.getActualNum(result)
        self.fh.SetCarry(result)
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_cpx(self):
        reg_x = self.cpu.x
        immediate = self.decoder.immediate
        result = reg_x - immediate
        result_8b = self.fh.getActualNum(result)
        self.fh.SetCarry(result)
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_cpy(self):
        reg_y = self.cpu.y
        immediate = self.decoder.immediate
        result = reg_y - immediate
        result_8b = self.fh.getActualNum(result)
        self.fh.SetCarry(result)
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_eor(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a ^ immediate
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_lda(self):
        immediate = self.decoder.immediate
        result_8b = self.fh.getActualNum(immediate)
        self.cpu.a = result_8b
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_ldx(self):
        immediate = self.decoder.immediate
        result_8b = self.fh.getActualNum(immediate)
        self.cpu.x = result_8b
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_ldy(self):
        immediate = self.decoder.immediate
        result_8b = self.fh.getActualNum(immediate)
        self.cpu.y = result_8b
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_ora(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a | immediate
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)

    def imd_sbc(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        carry = self.cpu.c
        result = reg_a - immediate - carry
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.SetCarry(result)
        self.fh.SetOverflow(reg_a, immediate, result_8b)
        self.fh.SetNegative(result_8b)
        self.fh.SetZero(result_8b)
