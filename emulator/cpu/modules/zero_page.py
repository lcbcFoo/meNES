from cpu.modules.flag_handler import FlagHandler

class ZeroPage():

        def __init__(self, cpu, mem, decoder):
            self.cpu = cpu
            self.mem = mem
            self.decoder = decoder
            self.fh = FlagHandler(cpu)

        # Adds value (inside given address) and carry to reg_a, puts result in
        # reg_a.
        # Flags: N, Z, C, V (from result).
        def zp_adc(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + oper + carry
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setOverflow(reg_a, oper, res_8b)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.immediate

        # "AND" between value (inside given address) and reg_a, puts result in
        # reg_a.
        # Flags: N, Z (from result).
        def zp_and(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a & oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.immediate

        # Shifts value (inside given address) 1 bit to the left, with bit 0 set
        # to 0. Result is stored in given address.
        # Flags: C -> bit 7 from initial value.
        #        N, Z (from result).
        def zp_asl(self):   #tested
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            res = oper << 1
            carry = (oper >> 7) & 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(carry)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # "AND" between value (inside given address) and reg_a, but does NOT put
        # result in reg_a.
        # Flags: N -> bit 7 from initial value.
        #        V -> bit 6 from initial value.
        #        Z (from result).
        def zp_bit(self):   #tested
            oper = self.decoder.cont_zp
            value_negative = (oper >> 7) & 1
            value_overflow = (oper >> 6) & 1
            res = self.cpu.a & oper
            self.fh.setZero(res)
            self.fh.forceNegativeFlag(value_negative)
            self.fh.forceOverflowFlag(value_overflow)
            return self.decoder.immediate

        # Subtracts the value (inside given address) from reg_a (reg_a - value).
        # Does NOT put result in reg_a or anywhere else.
        # Flags: Z, N, C (from result).
        def zp_cmp(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a + (~oper + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            return self.decoder.immediate

        # Subtracts the value (inside given address) from reg_x (reg_x - value).
        # Does NOT put result in reg_x or anywhere else.
        # Flags: Z, N, C (from result).
        def zp_cpx(self):   #tested
            oper = self.decoder.cont_zp
            reg_x = self.cpu.x
            res = reg_x + (~oper + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            return self.decoder.immediate

        # Subtracts the value (inside given address) from reg_y (reg_y - value).
        # Does NOT put result in reg_y or anywhere else.
        # Flags: Z, N, C (from result).
        def zp_cpy(self):   #tested
            oper = self.decoder.cont_zp
            reg_y = self.cpu.y
            res = reg_y + (~oper + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            return self.decoder.immediate

        # Subtracts 1 from value (inside given address) (result = value - 1)
        # and stores the result back in the given address.
        # Does NOT affect any register.
        # Flags: N, Z (from result).
        def zp_dec(self):   #tested
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            res = oper + (~1 + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # "XOR" between value (inside given address) and reg_a, puts result in
        # reg_a.
        # Flags: N, Z (from result).
        def zp_eor(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a ^ oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.immediate

        # Adds 1 to value (inside given address), stores result in given
        # address. Does NOT affect any register.
        # Flags: N, Z (from result).
        def zp_inc(self):   #tested
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            res_8b = self.fh.getActualNum(oper+1)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # Puts value (from given address) inside reg_a.
        # Flags: N, Z (from value).
        def zp_lda(self):  #tested
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.immediate

        # Puts value (from given address) inside reg_x.
        # Flags: N, Z (from value).
        def zp_ldx(self):  #tested
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.x = res_8b
            return self.decoder.immediate

        # Puts value (from given address) inside reg_y.
        # Flags: N, Z (from value).
        def zp_ldy(self):  #tested
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.y = res_8b
            return self.decoder.immediate

        # Shifts value (inside given address) 1 bit to the right, with bit 7 set
        # to 0. Result is stored in given address.
        # Flags: C -> bit 0 from initial value.
        #        N -> 0
        #        Z (from result)
        def zp_lsr(self):   #tested
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            carry = oper & 1
            res = oper >> 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(carry)
            self.fh.forceNegativeFlag(0)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # "OR" between value (from given address) and reg_a, puts result in
        # reg_a.
        # Flags: N, Z (from result).
        def zp_ora(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a | oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.immediate

        # Rotates value (from given address) 1 bit to the left, with initial
        # carry becoming bit 0. Stores result in given address.
        # Does NOT affect any register.
        # Flags: C -> bit 7 from inicial value.
        #        N, Z (from result).
        def zp_rol(self):   #tested
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            leftmost = (oper >> 7) & 1
            res = (oper << 1) + self.cpu.c
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(leftmost)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # Rotates value (from given address) 1 bit to the right, with initial
        # carry becoming bit 7. Stores result in given address.
        # Does NOT affect any register.
        # Flags: C -> bit 0 from inicial value.
        #        N, Z (from result).
        def zp_ror(self):   #tested
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            rightmost = oper & 1
            res = (self.cpu.c << 7) + (oper >> 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(rightmost)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # Subtracts the value (inside given address) and borrow from reg_a
        # (result = reg_a - value - carry), puts result in reg_a. Borrow is the
        # carry flag complemented.
        # Flags: C -> is set if result is >= 0.
        #        V -> is set when result > 127 ou result < -127.
        #        N, Z (from result)
        def zp_sbc(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + (~oper) + carry
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setOverflowSbc(reg_a, oper, carry, res_8b)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.immediate

        # Transfers content of reg_a to given address.
        # Does not affect any register or flags.
        def zp_sta(self):   #tested
            addr = self.decoder.immediate
            self.cpu.mem_bus.write(addr, self.cpu.a)
            return addr

        # Transfers content of reg_x to given address.
        # Does not affect any register or flags.
        def zp_stx(self):   #tested
            addr = self.decoder.immediate
            self.cpu.mem_bus.write(addr, self.cpu.x)
            return addr

        # Transfers content of reg_y to given address.
        # Does not affect any register or flags.
        def zp_sty(self):   #tested
            addr = self.decoder.immediate
            self.cpu.mem_bus.write(addr, self.cpu.y)
            return addr

        # Adds value (inside given [address + reg_x]) to reg_a, puts result in
        # reg_a.
        # Flags: N, Z, C, V (from result).
        def zpx_adc(self):  #tested
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + oper + carry
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setOverflow(reg_a, oper, res_8b)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.addr_x

        # "AND" between value (inside given address + reg_x) and reg_a, puts
        # result in reg_a.
        # Flags: N, Z (from result).
        def zpx_and(self):  #tested
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a & oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.addr_x

        # Shifts value (inside given address + reg_x) 1 bit to the left, with
        # bit 0 set to 0. Result is stored in [given address + reg_x].
        # Flags: C -> bit 7 from initial value.
        #        N, Z (from result).
        def zpx_asl(self):  #tested
            oper = self.decoder.cont_zp_x
            addr = self.decoder.addr_x
            res = oper << 1
            carry = (oper >> 7) & 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(carry)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # Subtracts the value (inside given address + reg_x) from reg_a
        # (reg_a - value).
        # Does NOT put result in reg_a or anywhere else.
        # Flags: Z, N, C (from result).
        def zpx_cmp(self):  #tested
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a + (~oper + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            return self.decoder.addr_x

        # Subtracts 1 from value (inside given address + reg_x)
        # (result = value - 1) and stores the result back in the given address.
        # Does NOT affect any register.
        # Flags: N, Z (from result).
        def zpx_dec(self):  #tested
            oper = self.decoder.cont_zp_x
            addr = self.decoder.addr_x
            res = oper + (~1 + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # "XOR" between value (inside given address + reg_x) and reg_a, puts
        # result in reg_a.
        # Flags: N, Z (from result).
        def zpx_eor(self):  #tested
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a ^ oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.addr_x

        # Adds 1 to value (inside given address + reg_x), stores result in given
        # [address + reg_x]. Does NOT affect any register.
        # Flags: N, Z (from result).
        def zpx_inc(self):  #tested
            oper = self.decoder.cont_zp_x
            addr = self.decoder.addr_x
            res_8b = self.fh.getActualNum(oper+1)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # Puts value (from given address + reg_x) inside reg_a.
        # Flags: N, Z (from value).
        def zpx_lda(self):  #tested
            oper = self.decoder.cont_zp_x
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.addr_x

        # Puts value (from given address + reg_x) inside reg_y.
        # Flags: N, Z (from value).
        def zpx_ldy(self):  #tested
            oper = self.decoder.cont_zp_x
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.y = res_8b
            return self.decoder.addr_x

        # Shifts value (inside given address + reg_x) 1 bit to the right, with
        # bit 7 set to 0. Result is stored in given [address + reg_x].
        # Flags: C -> bit 0 from initial value.
        #        N -> 0
        #        Z (from result)
        def zpx_lsr(self):  #tested
            oper = self.decoder.cont_zp_x
            addr = self.decoder.addr_x
            carry = oper & 1
            res = oper >> 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(carry)
            self.fh.forceNegativeFlag(0)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # "OR" between value (from given address + reg_x) and reg_a, puts
        # result in reg_a.
        # Flags: N, Z (from result).
        def zpx_ora(self):  #tested
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a | oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.addr_x

        # Rotates value (from given address + reg_x) 1 bit to the left, with
        # initial carry becoming bit 0. Stores result in [given address + reg_x].
        # Does NOT affect any register.
        # Flags: C -> bit 7 from inicial value.
        #        N, Z (from result).
        def zpx_rol(self):  #tested
            oper = self.decoder.cont_zp_x
            addr = self.decoder.addr_x
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
        def zpx_ror(self):  #tested
            oper = self.decoder.cont_zp_x
            addr = self.decoder.addr_x
            rightmost = oper & 1
            res = (self.cpu.c << 7) + (oper >> 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(rightmost)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)
            return addr

        # Subtracts the value (inside given address + reg_x) and borrow from
        # reg_a (result = reg_a - value - carry), puts result in reg_a.
        # Borrow is the carry flag complemented.
        # Flags: C -> is set if result is >= 0.
        #        V -> is set when result > 127 ou result < -127.
        #        N, Z (from result)
        def zpx_sbc(self):   #tested
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + (~oper) + carry
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setOverflowSbc(reg_a, oper, carry, res_8b)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b
            return self.decoder.addr_x

        # Transfers content of reg_a to [given address + reg_x].
        # Does not affect any register or flags.
        def zpx_sta(self):  #tested
            addr = self.decoder.addr_x
            self.cpu.mem_bus.write(addr, self.cpu.a)
            return addr

        # Transfers content of reg_y to [given address + reg_x].
        # Does not affect any register or flags.
        def zpx_sty(self):  #tested
            addr = self.decoder.addr_x
            self.cpu.mem_bus.write(addr, self.cpu.y)
            return addr

        # Puts value (from given address + reg_y) inside reg_x.
        # Flags: N, Z (from value).
        def zpy_ldx(self):  #tested
            oper = self.decoder.cont_zp_y
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.x = res_8b
            return self.decoder.addr_y

        # Transfers content of reg_x to [given address + reg_y].
        # Does not affect any register or flags.
        def zpy_stx(self):  #tested
            addr = self.decoder.addr_y
            self.cpu.mem_bus.write(addr, self.cpu.x)
            return addr
