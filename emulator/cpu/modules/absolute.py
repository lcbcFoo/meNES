from cpu.modules.decoder import Decoder
from cpu.modules.flag_handler import FlagHandler

class Absolute():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = self.cpu.flag_handler

    # Adds value (inside given address) to reg_a, puts result in reg_a.
    # Flags: N, Z, C, V (from result)
    # Tested
    def abs_adc(self):
        absolute = self.decoder.content
        result = self.cpu.a + absolute + self.cpu.c
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setCarry(result)
        self.fh.setOverflow(self.cpu.a, absolute, result_8b)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # "AND" between value (inside given address) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result)
    # Tested
    def abs_and(self):
        oper = self.decoder.content
        reg_a = self.cpu.a
        res = reg_a & oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

    # Shifts value (inside given address) 1 bit to the left, with
    # bit 0 set to 0. Result is stored in [given address].
    # Flags: C -> bit 7 from initial value.
    #        N, Z (from result).
    # Tested
    def abs_asl(self):
        oper = self.decoder.content
        addr = self.decoder.full_addr
        res = oper << 1
        carry = (oper >> 7) & 1
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(carry)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)

    # "AND" between value (inside given address) and reg_a, but does NOT put
    # result in reg_a.
    # Flags: N -> bit 7 from initial value.
    #        V -> bit 6 from initial value.
    #        Z (from result).
    def abs_bit(self):
        oper = self.decoder.content
        value_negative = (oper >> 7) & 1
        value_overflow = (oper >> 6) & 1
        res = self.cpu.a & oper
        self.fh.setZero(res)
        self.fh.forceNegativeFlag(value_negative)
        self.fh.forceOverflowFlag(value_overflow)

    # Subtracts the value (inside given address) from reg_a (reg_a - value).
    # Does NOT put result in reg_a or anywhere else.
    # Flags: Z, N, C (from result).
    # Tested
    def abs_cmp(self):
        oper = self.decoder.content
        result = self.cpu.a + (~oper + 1)
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarry(result)

    # Subtracts the value (inside given address) from reg_x (reg_x - value).
    # Does NOT put result in reg_x or anywhere else.
    # Flags: Z, N, C (from result).
    # Tested
    def abs_cpx(self):
        oper = self.decoder.content
        result = self.cpu.x + (~oper + 1)
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarry(result)

    # Subtracts the value (inside given address) from reg_y (reg_y - value).
    # Does NOT put result in reg_y or anywhere else.
    # Flags: Z, N, C (from result).
    # Tested
    def abs_cpy(self):
        oper = self.decoder.content
        result = self.cpu.y + (~oper + 1)
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarry(result)

    # Subtracts 1 from value (inside given address) (result = value - 1)
    # and stores the result back in the given address.
    # Does NOT affect any register.
    # Flags: N, Z (from result).
    def abs_dec(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = oper + (~1 + 1)
        result_8b = self.fh.getActualNum(result)
        self.cpu.mem_bus.write(oper_addr, result_8b, n=1)

    # "XOR" between value (inside given address) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result).
    # Tested
    def abs_eor(self):
        oper = self.decoder.content
        result = self.cpu.a ^ oper
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    # Adds 1 to value (inside given address), stores result in given
    # address. Does NOT affect any register.
    # Flags: N, Z (from result).
    # Tested
    def abs_inc(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = self.fh.getActualNum(oper+1)
        self.cpu.mem_bus.write(oper_addr, result, n=1)

    # Probably is incomplete since doesn't check page
    def abs_jmp(self):
    #     oper = self.decoder.content
    #     self.cpu.pc = oper
        pass

    def abs_jsr(self):
    #     oper = self.decoder.content
        pass
    
    # Data is transferred from memory to the accumulator and stored in reg_a
    # Flags: N, Z (from value).
    # Tested
    def abs_lda(self):
        oper = self.decoder.content
        result = self.fh.getActualNum(oper)
        self.cpu.a = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

    # Data is transferred from memory to the accumulator and stored in reg_x
    # Flags: N, Z (from value).
    # Tested
    def abs_ldx(self):
        oper = self.decoder.content
        result = self.fh.getActualNum(oper)
        self.cpu.x = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

    # Data is transferred from memory to the accumulator and stored in reg_y
    # Flags: N, Z (from value).
    # Tested
    def abs_ldy(self):
        oper = self.decoder.content
        result = self.fh.getActualNum(oper)
        self.cpu.y = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

    # Shifts value (inside given address) 1 bit to the right, with bit 7 set
    # to 0. Result is stored in given address.
    # Flags: C -> bit 0 from initial value.
    #        N -> 0
    #        Z (from result)
    # Tested
    def abs_lsr(self):
        oper = self.decoder.content
        addr = self.decoder.full_addr
        carry = oper & 1
        res = oper >> 1
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(carry)
        self.fh.setNegative(res_8b)
        self.fh.forceZeroFlag(0)
        self.cpu.mem_bus.write(addr, res_8b)

    # "OR" between value (from given address) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result).
    #Tested
    def abs_ora(self):
        oper = self.decoder.content
        result = self.cpu.a | oper
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    def abs_rol(self):
    #     oper = self.decoder.content
    #     oper_addr = self.decoder.full_addr
    #     result = oper << 1
    #     result_8b = self.fh.getActualNum(result)
    #     self.fh.setNegative(result_8b)
    #     self.fh.setZero(result_8b)
    #     self.fh.setCarry(result)

    #     # sets bit 0 to carry bit
    #     if self.cpu.c & 1 == 1:
    #         result = result | 1

    #     # sets carry bit to bit 7
        
    #     self.cpu.mem_bus.write(oper_addr, result, n=1)
        pass

    def abs_ror(self):
    #     oper = self.decoder.content
    #     oper_addr = self.decoder.full_addr
    #     new_carry = oper & 1 == 1 # Gets carry bit info
    #     new_bit_7 = self.cpu.c
    #     result = oper >> 1
    #     result = new_bit_7 <
    #     result_8b = self.fh.getActualNum(result)
    #     self.fh.setNegative(result_8b)
    #     self.fh.setZero(result_8b)
    #     self.fh.setCarry(result)

    #     # sets carry bit to bit 7
    #     if new_carry:
    #         self.cpu.c = 1
    #     else:
    #         self.cpu.c = 0


    #     # set bit 0 to carry bit
        
    #     self.cpu.mem_bus.write(oper_addr, result, n=1)
        pass

    # Subtracts the value (inside given address) and borrow from reg_a
    # (result = reg_a - value - carry), puts result in reg_a. Borrow is the
    # carry flag complemented.
    # Flags: C -> is set if result is >= 0.  -- CHANGE LATER
    #        V -> is set when result > 127 ou result < -127.
    #        N, Z (from result)
    # test_made -> check carry influence
    def abs_sbc(self):
        oper = self.decoder.content
        reg_a = self.cpu.a
        borrow = (~self.cpu.c + 1)
        res = reg_a + (~oper + 1) + borrow
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarrySbc(res)
        self.fh.setOverflowSbc(res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res

    # Transfers content of reg_a to given address.
    # Does not affect any register or flags.
    # Tested
    def abs_sta(self):
        oper = self.decoder.full_addr
        self.cpu.mem_bus.write(oper, self.cpu.a, n=1)

    # Transfers content of reg_x to given address.
    # Does not affect any register or flags.
    def abs_stx(self):
        oper = self.decoder.full_addr
        self.cpu.mem_bus.write(oper, self.cpu.x, n=1)

    # Transfers content of reg_y to given address.
    # Does not affect any register or flags.
    def abs_sty(self):
        oper = self.decoder.full_addr
        self.cpu.mem_bus.write(oper, self.cpu.y, n=1)

    ###################################################################################################################
    ############### ABSOLUTE X OPERATIONS #############################################################################
    ###################################################################################################################

    def absX_adc(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a + absolute_x + self.cpu.c
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setCarry(result)
        self.fh.setOverflow(self.cpu.a, absolute_x, result_8b)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    def absX_and(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a & absolute_x
        self.fh.setNegative(result)
        self.fh.setZero(result)

    def absX_asl(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr + self.cpu.x
        result = absolute_x << 1
        result_8b = self.fh.getActualNum(result)
        self.cpu.mem_bus.write(oper_addr, result_8b, n=1)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarry(result)

    def absX_cmp(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a - absolute_x
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarry(result)

    def absX_dec(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr + self.cpu.x
        result = self.fh.getActualNum(absolute_x-1)
        self.cpu.mem_bus.write(oper_addr, result, n=1)


    def absX_eor(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a ^ absolute_x
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    def absX_inc(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr + self.cpu.x
        result = self.fh.getActualNum(absolute_x+1)
        self.cpu.mem_bus.write(oper_addr, result, n=1)


    def absX_lda(self):
        absolute_x = self.decoder.content_x
        result = self.fh.getActualNum(absolute_x)
        self.cpu.a = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

    def absX_ldy(self):
        absolute_x = self.decoder.content_x
        result = self.fh.getActualNum(absolute_x)
        self.cpu.y = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

    def absX_lsr(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr + self.cpu.x
        result = absolute_x >> 1
        result_8b = self.fh.getActualNum(result)
        self.cpu.mem_bus.write(oper_addr, result_8b, n=1)
        self.fh.setNegative(result_8b)
        self.fh.forceZeroFlag(0)
        self.fh.setCarry(result)

    def absX_ora(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a | absolute_x
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    def absX_rol(self):
        pass

    def absX_ror(self):
        pass

    def absX_sbc(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a - absolute_x - self.cpu.c
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setOverflow(result_8b)
        self.fh.setCarry(result)

    def absX_sta(self):
        absolute_x = self.decoder.full_addr + self.cpu.x
        address = self.fh.getActualNum(absolute_x)
        self.cpu.mem_bus.write(address, self.cpu.a, n=1)


    ###################################################################################################################
    ############### ABSOLUTE Y OPERATIONS #############################################################################
    ###################################################################################################################

    def absY_adc(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a + absolute_y + self.cpu.c
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setCarry(result)
        self.fh.setOverflow(self.cpu.a, absolute_y, result_8b)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    def absY_and(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a & absolute_y
        self.fh.setNegative(result)
        self.fh.setZero(result)

    def absY_cmp(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a - absolute_y
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarry(result)

    def absY_eor(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a ^ absolute_y
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    def absY_lda(self):
        absolute_y = self.decoder.content_y
        result = self.fh.getActualNum(absolute_y)
        self.cpu.a = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

    def absY_ldx(self):
        absolute_y = self.decoder.content_y
        result = self.fh.getActualNum(absolute_y)
        self.cpu.x = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

    def absY_ora(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a | absolute_y
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

    def absY_sbc(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a - absolute_y - self.cpu.c
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setOverflow(result_8b)
        self.fh.setCarry(result)

    def absY_sta(self):
        absolute_y = self.decoder.full_addr + self.cpu.y
        address = self.fh.getActualNum(absolute_y)
        self.cpu.mem_bus.write(address, self.cpu.a, n=1)
