from cpu.modules.flag_handler import FlagHandler

class Immediate():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    # Adds value from immediate to reg_a, puts result in reg_a.
    # Flags: N, Z, C, V (from result)
    def imd_adc(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        carry = self.cpu.c
        result = reg_a + immediate + carry
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setCarry(result)
        self.fh.setOverflow(reg_a, immediate, result_8b)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # "AND" between value of immediate and reg_a, puts result in reg_a.
    # Flags: N, Z (from result)
    def imd_and(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a & immediate
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Subtracts the value of immediate from reg_a (reg_a - value).
    # Does NOT put result in reg_a or anywhere else.
    # Flags: Z, N, C (from result).
    def imd_cmp(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a + (~immediate + 1)
        result_8b = self.fh.getActualNum(result)
        if(immediate <= reg_a):
            self.fh.forceCarryFlag(1)
        else:
            self.fh.forceCarryFlag(0)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Subtracts the value of immediate from reg_x (reg_x - value).
    # Does NOT put result in reg_x or anywhere else.
    # Flags: Z, N, C (from result).
    def imd_cpx(self):
        reg_x = self.cpu.x
        immediate = self.decoder.immediate
        result = reg_x + (~immediate + 1)
        result_8b = self.fh.getActualNum(result)
        if(immediate <= reg_x):
            self.fh.forceCarryFlag(1)
        else:
            self.fh.forceCarryFlag(0)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Subtracts the value of immediate from reg_y (reg_y - value).
    # Does NOT put result in reg_y or anywhere else.
    # Flags: Z, N, C (from result).
    def imd_cpy(self):
        reg_y = self.cpu.y
        immediate = self.decoder.immediate
        result = reg_y + (~immediate + 1)
        result_8b = self.fh.getActualNum(result)
        if(immediate <= reg_y):
            self.fh.forceCarryFlag(1)
        else:
            self.fh.forceCarryFlag(0)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # "XOR" between value of immediate and reg_a, puts result in reg_a.
    # Flags: N, Z (from result).
    def imd_eor(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a ^ immediate
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Puts value of immediate inside reg_a.
    # Flags: N, Z (from value).
    def imd_lda(self):
        immediate = self.decoder.immediate
        result_8b = self.fh.getActualNum(immediate)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Puts value of immediate inside reg_x.
    # Flags: N, Z (from value).
    def imd_ldx(self):
        immediate = self.decoder.immediate
        result_8b = self.fh.getActualNum(immediate)
        self.cpu.x = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Puts value of immediate inside reg_y.
    # Flags: N, Z (from value).
    def imd_ldy(self):
        immediate = self.decoder.immediate
        result_8b = self.fh.getActualNum(immediate)
        self.cpu.y = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # "OR" between value of immediate and reg_a, puts result in reg_a.
    # Flags: N, Z (from result).
    def imd_ora(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        result = reg_a | immediate
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Subtracts the value of immediate and borrow from reg_a
    # (result = reg_a - value - borrow), puts result in reg_a. Borrow is the
    # carry flag complemented.
    # Flags: C -> is set if result is >= 0.  -- CHANGE LATER
    #        V -> is set when result > 127 ou result < -127.
    #        N, Z (from result)
    def imd_sbc(self):
        reg_a = self.cpu.a
        immediate = self.decoder.immediate
        carry = self.cpu.c
        result = reg_a + (~immediate +1) + (~carry + 1)
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setCarrySbc(result)
        self.fh.setOverflowSbc(reg_a, immediate, result_8b)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
