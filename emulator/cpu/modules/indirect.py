from cpu.modules.flag_handler import FlagHandler

class Indirect():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    # JMP transfers program execution to the location contained in the
    # following address (indirect).
    def ind_jmp(self):
        addr = self.decoder.pointer_addr
        self.cpu.pc = addr
        self.cpu.update_pc = False

    # Adds value from pointer_content_x to reg_a, puts result in reg_a.
    # Flags: N, Z, C, V (from result)
    def indx_adc(self):
        oper = self.decoder.pointer_content_x
        reg_a = self.cpu.a
        carry = self.cpu.c
        res = reg_a + oper + carry
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarry(res)
        self.fh.setOverflow(reg_a, oper, res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # "AND" between value of pointer_content_x and reg_a, puts result in reg_a.
    # Flags: N, Z (from result)
    def indx_and(self):
        oper = self.decoder.pointer_content_x
        reg_a = self.cpu.a
        res = reg_a & oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Subtracts the value of pointer_content_x from reg_a (reg_a - value).
    # Does NOT put result in reg_a or anywhere else.
    # Flags: Z, N, C (from result).
    def indx_cmp(self):
        oper = self.decoder.pointer_content_x
        reg_a = self.cpu.a
        res = reg_a + (~oper + 1)
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarrySbc(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)

    # "XOR" between value of pointer_content_x and reg_a, puts result in reg_a.
    # Flags: N, Z (from result).
    def indx_eor(self):
        oper = self.decoder.pointer_content_x
        reg_a = self.cpu.a
        res = reg_a ^ oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Puts value of pointer_content_x inside reg_a.
    # Flags: N, Z (from value).
    def indx_lda(self):
        oper = self.decoder.pointer_content_x
        res_8b = self.fh.getActualNum(oper)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b
        return self.decoder.pointer_addr_x

    # "OR" between value of pointer_content_x and reg_a, puts result in reg_a.
    # Flags: N, Z (from result).
    def indx_ora(self):
        oper = self.decoder.pointer_content_x
        reg_a = self.cpu.a
        res = reg_a | oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Subtracts the value of pointer_content_x and borrow from reg_a
    # (result = reg_a - value - borrow), puts result in reg_a. Borrow is the
    # carry flag complemented.
    # Flags: C -> is set if result is >= 0.  -- CHANGE LATER
    #        V -> is set when result > 127 ou result < -127.
    #        N, Z (from result)
    def indx_sbc(self):
        oper = self.decoder.pointer_content_x
        reg_a = self.cpu.a
        carry = self.cpu.c
        res = reg_a + (~oper + 1) + carry - 1
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarrySbc(res)
        self.fh.setOverflowSbc(reg_a, oper, carry, res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Transfers content of reg_a to pointer_content_x address.
    # Does not affect any register or flags.
    def indx_sta(self):
        addr = self.decoder.pointer_addr_x
        self.cpu.mem_bus.write(addr, self.cpu.a)
        return addr

    ##########################################################################
    #
    # ind Y
    #
    ##########################################################################

    # Adds value from pointer_content_y to reg_a, puts result in reg_a.
    # Flags: N, Z, C, V (from result)
    def indy_adc(self):
        reg_a = self.cpu.a
        v = self.decoder.pointer_content_y
        carry = self.cpu.c
        result = reg_a + v + carry
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setCarry(result)
        self.fh.setOverflow(reg_a, v, result_8b)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)


    # "AND" between value of pointer_content_y and reg_a, puts result in reg_a.
    # Flags: N, Z (from result)
    def indy_and(self):
        reg_a = self.cpu.a
        v = self.decoder.pointer_content_y
        result = reg_a & v
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Subtracts the value of pointer_content_y from reg_a (reg_a - value).
    # Does NOT put result in reg_a or anywhere else.
    # Flags: Z, N, C (from result).
    def indy_cmp(self):
        oper = self.decoder.pointer_content_y
        reg_a = self.cpu.a
        res = reg_a + (~oper + 1)
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarrySbc(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)

    # "XOR" between value of pointer_content_y and reg_a, puts result in reg_a.
    # Flags: N, Z (from result).
    def indy_eor(self):
        oper = self.decoder.pointer_content_y
        reg_a = self.cpu.a
        res = reg_a ^ oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Puts value of pointer_content_y inside reg_a.
    # Flags: N, Z (from value).
    def indy_lda(self):
        oper = self.decoder.pointer_content_y
        res_8b = self.fh.getActualNum(oper)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b
        return self.decoder.pointer_addr_y

    # "OR" between value of pointer_content_y and reg_a, puts result in reg_a.
    # Flags: N, Z (from result).
    def indy_ora(self):
        oper = self.decoder.pointer_content_y
        reg_a = self.cpu.a
        res = reg_a | oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Subtracts the value of pointer_content_y and borrow from reg_a
    # (result = reg_a - value - borrow), puts result in reg_a. Borrow is the
    # carry flag complemented.
    # Flags: C -> is set if result is >= 0.  -- CHANGE LATER
    #        V -> is set when result > 127 ou result < -127.
    #        N, Z (from result)
    def indy_sbc(self):
        oper = self.decoder.pointer_content_y
        reg_a = self.cpu.a
        carry = self.cpu.c
        res = reg_a + (~oper + 1) + carry - 1
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarrySbc(res)
        self.fh.setOverflowSbc(reg_a, oper, carry, res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Transfers content of reg_a to pointer_content_y address.
    # Does not affect any register or flags.
    def indy_sta(self):
        addr = self.decoder.pointer_addr_y
        self.cpu.mem_bus.write(addr, self.cpu.a)
        return addr
