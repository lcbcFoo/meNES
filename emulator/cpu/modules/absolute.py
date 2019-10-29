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
        return self.decoder.full_addr

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
        return self.decoder.full_addr


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
        return self.decoder.full_addr


    # "AND" between value (inside given address) and reg_a, but does NOT put
    # result in reg_a.
    # Flags: N -> bit 7 from initial value.
    #        V -> bit 6 from initial value.
    #        Z (from result).
    #Tested
    def abs_bit(self):
        oper = self.decoder.content
        value_negative = (oper >> 7) & 1
        value_overflow = (oper >> 6) & 1
        res = self.cpu.a & oper
        self.fh.setZero(res)
        self.fh.forceNegativeFlag(value_negative)
        self.fh.forceOverflowFlag(value_overflow)
        return self.decoder.full_addr

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
        self.fh.setCarrySbc(result)
        return self.decoder.full_addr

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
        self.fh.setCarrySbc(result)
        return self.decoder.full_addr

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
        self.fh.setCarrySbc(result)
        return self.decoder.full_addr

    # Subtracts 1 from value (inside given address) (result = value - 1)
    # and stores the result back in the given address.
    # Does NOT affect any register.
    # Flags: N, Z (from result).
    # Tested
    def abs_dec(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = oper + (~1 + 1)
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.cpu.mem_bus.write(oper_addr, result_8b, n=1)
        return self.decoder.full_addr

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
        return self.decoder.full_addr

    # Adds 1 to value (inside given address), stores result in given
    # address. Does NOT affect any register.
    # Flags: N, Z (from result).
    # Tested
    def abs_inc(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = self.fh.getActualNum(oper+1)
        self.fh.setNegative(result)
        self.fh.setZero(result)
        self.cpu.mem_bus.write(oper_addr, result, n=1)
        return self.decoder.full_addr

    # JMP changes pc to the following address
    # No flags are affected.
    # Tested
    def abs_jmp(self):
        oper = self.decoder.full_addr
        self.cpu.pc = oper
        self.cpu.update_pc = False

    def abs_jsr(self):
        next_pc = self.cpu.pc + 2
        PCH = (next_pc >> 8) & 255
        self.cpu.push_stack(PCH)
        PCL = next_pc & 255
        self.cpu.push_stack(PCL)
        oper = self.decoder.full_addr
        self.cpu.pc = oper
        self.cpu.update_pc = False

    # Data is transferred from memory to the accumulator and stored in reg_a
    # Flags: N, Z (from value).
    # Tested
    def abs_lda(self):
        oper = self.decoder.content
        result = self.fh.getActualNum(oper)
        self.cpu.a = result
        self.fh.setNegative(result)
        self.fh.setZero(result)
        return self.decoder.full_addr

    # Data is transferred from memory to the accumulator and stored in reg_x
    # Flags: N, Z (from value).
    # Tested
    def abs_ldx(self):
        oper = self.decoder.content
        result = self.fh.getActualNum(oper)
        self.cpu.x = result
        self.fh.setNegative(result)
        self.fh.setZero(result)
        return self.decoder.full_addr

    # Data is transferred from memory to the accumulator and stored in reg_y
    # Flags: N, Z (from value).
    # Tested
    def abs_ldy(self):
        oper = self.decoder.content
        result = self.fh.getActualNum(oper)
        self.cpu.y = result
        self.fh.setNegative(result)
        self.fh.setZero(result)
        return self.decoder.full_addr

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
        self.fh.forceNegativeFlag(0)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)
        return self.decoder.full_addr

    # "OR" between value (from given address) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result).
    # Tested
    def abs_ora(self):
        oper = self.decoder.content
        result = self.cpu.a | oper
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        return self.decoder.full_addr

    # Rotates value (from given address) 1 bit to the left, with initial
    # carry becoming bit 0. Stores result in given address.
    # Does NOT affect any register.
    # Flags: C -> bit 7 from inicial value.
    #        N, Z (from result).
    # Tested
    def abs_rol(self):
        oper = self.decoder.content
        addr = self.decoder.full_addr
        leftmost = (oper >> 7) & 1
        res = (oper << 1) + self.cpu.c
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(leftmost)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)
        return self.decoder.full_addr

    # Rotates value (from given address) 1 bit to the right, with initial
    # carry becoming bit 7. Stores result in given address.
    # Does NOT affect any register.
    # Flags: C -> bit 0 from inicial value.
    #        N, Z (from result).
    # Tested
    def abs_ror(self):
        oper = self.decoder.content
        addr = self.decoder.full_addr
        rightmost = oper & 1
        res = (self.cpu.c << 7) + (oper >> 1)
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(rightmost)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)
        return self.decoder.full_addr

    # Subtracts the value (inside given address) and borrow from reg_a
    # (result = reg_a - value - carry), puts result in reg_a. Borrow is the
    # carry flag complemented.
    # Flags: C -> is set if result is >= 0.  -- CHANGE LATER
    #        V -> is set when result > 127 ou result < -127.
    #        N, Z (from result)
    # Tested
    def abs_sbc(self):
        reg_a = self.cpu.a
        oper = self.decoder.content
        carry = self.cpu.c
        result = reg_a + (~oper) + carry
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setCarrySbc(result)
        self.fh.setOverflowSbc(reg_a, oper, carry, result_8b)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        return self.decoder.full_addr

    # Transfers content of reg_a to given address.
    # Does not affect any register or flags.
    # Tested
    def abs_sta(self):
        oper = self.decoder.full_addr
        self.cpu.mem_bus.write(oper, self.cpu.a, n=1)
        return self.decoder.full_addr

    # Transfers content of reg_x to given address.
    # Does not affect any register or flags.
    def abs_stx(self):
        oper = self.decoder.full_addr
        self.cpu.mem_bus.write(oper, self.cpu.x, n=1)
        return self.decoder.full_addr

    # Transfers content of reg_y to given address.
    # Does not affect any register or flags.
    def abs_sty(self):
        oper = self.decoder.full_addr
        self.cpu.mem_bus.write(oper, self.cpu.y, n=1)
        return self.decoder.full_addr

    ###################################################################################################################
    ############### ABSOLUTE X OPERATIONS #############################################################################
    ###################################################################################################################

    # Adds value (inside given [address + reg_x]) to reg_a, puts result in
    # reg_a.
    # Flags: N, Z, C, V (from result).
    # Tested
    def absX_adc(self):
        oper = self.decoder.content_x
        reg_a = self.cpu.a
        carry = self.cpu.c
        res = reg_a + oper + carry
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarry(res)
        self.fh.setOverflow(reg_a, oper, res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # "AND" between value (inside given address +reg_x) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result)
    # Tested
    def absX_and(self):
        oper = self.decoder.content_x
        reg_a = self.cpu.a
        res = reg_a & oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # Shifts value (inside given address + reg_x) 1 bit to the left, with
    # bit 0 set to 0. Result is stored in [given address].
    # Flags: C -> bit 7 from initial value.
    #        N, Z (from result).
    # Tested
    def absX_asl(self):
        oper = self.decoder.content_x
        addr = self.decoder.full_addr_x
        res = oper << 1
        carry = (oper >> 7) & 1
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(carry)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)
        return addr

    # Subtracts the value (inside given address + reg_x) from reg_a (reg_a - value).
    # Does NOT put result in reg_a or anywhere else.
    # Flags: Z, N, C (from result).
    # Tested
    def absX_cmp(self):
        oper = self.decoder.content_x
        result = self.cpu.a + (~oper + 1)
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarrySbc(result)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # Subtracts 1 from value (inside given address + reg_x) (result = value - 1)
    # and stores the result back in the given address.
    # Does NOT affect any register.
    # Flags: N, Z (from result).
    # Tested
    def absX_dec(self):
        oper = self.decoder.content_x
        oper_addr = self.decoder.full_addr_x
        result = oper + (~1 + 1)
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.cpu.mem_bus.write(oper_addr, result_8b, n=1)
        return oper_addr

    # "XOR" between value (inside given address + reg_x) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result).
    # Tested
    def absX_eor(self):
        oper = self.decoder.content_x
        result = self.cpu.a ^ oper
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # Adds 1 to value (inside given address + reg_x), stores result in given
    # address. Does NOT affect any register.
    # Flags: N, Z (from result).
    # Tested
    def absX_inc(self):
        oper = self.decoder.content_x
        oper_addr = self.decoder.full_addr_x
        result = self.fh.getActualNum(oper+1)
        self.fh.setNegative(result)
        self.fh.setZero(result)
        self.cpu.mem_bus.write(oper_addr, result, n=1)
        return oper_addr

    # Puts value (from given address + reg_x) inside reg_a.
    # Flags: N, Z (from value).
    # Tested
    def absX_lda(self):
        oper = self.decoder.content_x
        result = self.fh.getActualNum(oper)
        self.cpu.a = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # Puts value (from given address + reg_x) inside reg_y.
    # Flags: N, Z (from value).
    # Tested
    def absX_ldy(self):
        oper = self.decoder.content_x
        result = self.fh.getActualNum(oper)
        self.cpu.y = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # Shifts value (inside given address + reg_x) 1 bit to the right, with bit 7 set
    # to 0. Result is stored in given address.
    # Flags: C -> bit 0 from initial value.
    #        N -> 0
    #        Z (from result)
    # Tested
    def absX_lsr(self):
        oper = self.decoder.content_x
        addr = self.decoder.full_addr_x
        carry = oper & 1
        res = oper >> 1
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(carry)
        self.fh.forceNegativeFlag(0)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)
        return addr

    # "OR" between value (from given address + reg_x) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result).
    # Tested
    def absX_ora(self):
        oper = self.decoder.content_x
        reg_a = self.cpu.a
        res = reg_a | oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # Rotates value (from given address + reg_x) 1 bit to the left, with
    # initial carry becoming bit 0. Stores result in [given address + reg_x].
    # Does NOT affect any register.
    # Flags: C -> bit 7 from inicial value.
    #        N, Z (from result).
    # Tested
    def absX_rol(self):
        oper = self.decoder.content_x
        addr = self.decoder.full_addr_x
        leftmost = (oper >> 7) & 1
        res = (oper << 1) + self.cpu.c
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(leftmost)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)
        return addr

    # Rotates value (from given address + reg_x) 1 bit to the right, with
    # initial carry becoming bit 7. Stores result in [given address + reg_x].
    # Does NOT affect any register.
    # Flags: C -> bit 0 from inicial value.
    #        N, Z (from result).
    # Tested
    def absX_ror(self):
        oper = self.decoder.content_x
        addr = self.decoder.full_addr_x
        rightmost = oper & 1
        res = (self.cpu.c << 7) + (oper >> 1)
        res_8b = self.fh.getActualNum(res)
        self.fh.forceCarryFlag(rightmost)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.mem_bus.write(addr, res_8b)
        return addr

    # Subtracts the value (inside given address + reg_x) and borrow from reg_a
    # (result = reg_a - value - carry), puts result in reg_a. Borrow is the
    # carry flag complemented.
    # Flags: C -> is set if result is >= 0.  -- CHANGE LATER
    #        V -> is set when result > 127 ou result < -127.
    #        N, Z (from result)
    # Tested
    def absX_sbc(self):
        oper = self.decoder.content_x
        reg_a = self.cpu.a
        carry = self.cpu.c
        res = reg_a + (~oper) + carry
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarrySbc(res)
        self.fh.setOverflowSbc(reg_a, oper, carry, res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_x
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_x

    # Transfers content of reg_a to given address + reg_x.
    # Does not affect any register or flags.
    # Tested
    def absX_sta(self):
        oper = self.decoder.full_addr_x
        self.cpu.mem_bus.write(oper, self.cpu.a, n=1)
        return oper


    ###################################################################################################################
    ############### ABSOLUTE Y OPERATIONS #############################################################################
    ###################################################################################################################

    # Adds value (inside given [address + reg_y]) to reg_a, puts result in
    # reg_a.
    # Flags: N, Z, C, V (from result).
    # Tested
    def absY_adc(self):
        oper = self.decoder.content_y
        reg_a = self.cpu.a
        carry = self.cpu.c
        res = reg_a + oper + carry
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarry(res)
        self.fh.setOverflow(reg_a, oper, res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # "AND" between value (inside given address +reg_y) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result)
    #Tested
    def absY_and(self):
        oper = self.decoder.content_y
        reg_a = self.cpu.a
        res = reg_a & oper
        res_8b = self.fh.getActualNum(res)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # Subtracts the value (inside given address + reg_x) from reg_a (reg_a - value).
    # Does NOT put result in reg_a or anywhere else.
    # Flags: Z, N, C (from result).
    # Tested
    def absY_cmp(self):
        oper = self.decoder.content_y
        result = self.cpu.a + (~oper + 1)
        result_8b = self.fh.getActualNum(result)
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)
        self.fh.setCarrySbc(result)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # "XOR" between value (inside given address + reg_x) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result).
    # Tested
    def absY_eor(self):
        oper = self.decoder.content_y
        result = self.cpu.a ^ oper
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # Puts value (from given address + reg_y) inside reg_a.
    # Flags: N, Z (from value).
    # Tested
    def absY_lda(self):
        oper = self.decoder.content_y
        result = self.fh.getActualNum(oper)
        self.cpu.a = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # Puts value (from given address + reg_y) inside reg_x.
    # Flags: N, Z (from value).
    # Tested
    def absY_ldx(self):
        oper = self.decoder.content_y
        result = self.fh.getActualNum(oper)
        self.cpu.x = result
        self.fh.setNegative(result)
        self.fh.setZero(result)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # "OR" between value (from given address + reg_y) and reg_a, puts result in
    # reg_a.
    # Flags: N, Z (from result).
    # Tested
    def absY_ora(self):
        oper = self.decoder.content_y
        result = self.cpu.a | oper
        result_8b = self.fh.getActualNum(result)
        self.cpu.a = result_8b
        self.fh.setNegative(result_8b)
        self.fh.setZero(result_8b)

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # Subtracts the value (inside given address + reg_y) and borrow from reg_a
    # (result = reg_a - value - carry), puts result in reg_a. Borrow is the
    # carry flag complemented.
    # Flags: C -> is set if result is >= 0.  -- CHANGE LATER
    #        V -> is set when result > 127 ou result < -127.
    #        N, Z (from result)
    # Tested
    def absY_sbc(self):
        oper = self.decoder.content_y
        reg_a = self.cpu.a
        carry = self.cpu.c
        res = reg_a + (~oper) + carry
        res_8b = self.fh.getActualNum(res)
        self.fh.setCarrySbc(res)
        self.fh.setOverflowSbc(reg_a, oper, carry, res_8b)
        self.fh.setNegative(res_8b)
        self.fh.setZero(res_8b)
        self.cpu.a = res_8b

        # Adds additional cycle if necessary
        addr = self.decoder.full_addr_y
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(addr)
        return self.decoder.full_addr_y

    # Transfers content of reg_a to given address + reg_y.
    # Does not affect any register or flags.
    # Tested
    def absY_sta(self):
        oper = self.decoder.full_addr_y
        self.cpu.mem_bus.write(oper, self.cpu.a, n=1)
        return oper
