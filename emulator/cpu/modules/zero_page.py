from cpu.modules.flag_handler import FlagHandler

class ZeroPage():

        def __init__(self, cpu, mem, decoder):
            self.cpu = cpu
            self.mem = mem
            self.decoder = decoder
            self.fh = FlagHandler(cpu)

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

        def zp_and(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a & oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_asl(self):   #tested
            oper = self.decoder.cont_zp
            res = oper << 1
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_bit(self):
            oper = self.decoder.cont_zp
            value_negative = (oper >> 7) & 1
            value_overflow = (oper >> 6) & 1
            res = self.cpu.a & oper
            self.fh.setZero(res)
            self.fh.forceNegativeFlag(value_negative)
            self.fh.forceOverflowFlag(value_overflow)

        def zp_cmp(self):   #tested
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a - oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)

        def zp_cpx(self):   #tested
            oper = self.decoder.cont_zp
            reg_x = self.cpu.x
            res = reg_x - oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)

        def zp_cpy(self):   #tested
            oper = self.decoder.cont_zp
            reg_y = self.cpu.y
            res = reg_y - oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)

        def zp_dec(self):
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            res_8b = self.fh.getActualNum(oper-1)
            self.cpu.mem_bus.write(addr, res_8b)

        def zp_eor(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a ^ oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_inc(self):   #tested
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            res_8b = self.fh.getActualNum(oper+1)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zp_lda(self):   #tested
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_ldx(self):   #tested
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.x = res_8b

        def zp_ldy(self):   #tested
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.y = res_8b

        def zp_lsr(self):
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            res = oper >> 1
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zp_ora(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a | oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_rol(self):
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            leftmost = (oper >> 7) & 1
            res = oper << 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(leftmost)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zp_ror(self):
            oper = self.decoder.cont_zp
            addr = self.decoder.immediate
            rightmost = oper & 1
            res = (self.cpu.c << 7) + oper >> 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(rightmost)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zp_sbc(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + (~oper + 1) + (~carry + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setOverflow(reg_a, oper, res_8b)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res

        def zp_sta(self):   #tested
            addr = self.decoder.immediate
            self.cpu.mem_bus.write(addr, self.cpu.a)

        def zp_stx(self):
            addr = self.decoder.immediate
            self.cpu.mem_bus.write(addr, self.cpu.x)

        def zp_sty(self):
            addr = self.decoder.immediate
            self.cpu.mem_bus.write(addr, self.cpu.y)

        def zpx_adc(self, X):
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

        def zpx_and(self, X):
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a & oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zpx_asl(self, X):
            oper = self.decoder.cont_zp_x
            res = oper << 1
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zpx_cmp(self, X):
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a - oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)

        def zpx_dec(self, X):
            oper = self.decoder.cont_zp_x
            addr = self.decoder.immediate + self.cpu.x
            res_8b = self.fh.getActualNum(oper-1)
            self.cpu.mem_bus.write(addr, res_8b)

        def zpx_eor(self, X):
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a ^ oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zpx_inc(self, X):
            oper = self.decoder.cont_zp_x
            addr = self.decoder.immediate + self.cpu.x
            res_8b = self.fh.getActualNum(oper+1)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zpx_lda(self, X):
            oper = self.decoder.cont_zp_x
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zpx_ldy(self, X):
            oper = self.decoder.cont_zp_x
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.y = res_8b

        def zpx_lsr(self, X):
            oper = self.decoder.cont_zp_x
            addr = self.decoder.immediate + self.cpu.x
            res = oper >> 1
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zpx_ora(self, X):
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a | oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zpx_rol(self, X):
            oper = self.decoder.cont_zp_x
            addr = self.decoder.immediate + self.cpu.x
            leftmost = (oper >> 7) & 1
            res = oper << 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(leftmost)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zpx_ror(self, X):
            oper = self.decoder.cont_zp_x
            addr = self.decoder.immediate + self.cpu.x
            rightmost = oper & 1
            res = (self.cpu.c << 7) + oper >> 1
            res_8b = self.fh.getActualNum(res)
            self.fh.forceCarryFlag(rightmost)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.mem_bus.write(addr, res_8b)

        def zpx_sbc(self, X):
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + (~oper + 1) + (~carry + 1)
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarrySbc(res)
            self.fh.setOverflow(reg_a, oper, res_8b)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res

        def zpx_sta(self, X):
            addr = self.decoder.immediate + self.cpu.x
            self.cpu.mem_bus.write(addr, self.cpu.a)

        def zpx_sty(self, X):
            addr = self.decoder.immediate + self.cpu.x
            self.cpu.mem_bus.write(addr, self.cpu.y)

        def zpy_ldx(self, Y):
            oper = self.decoder.cont_zp_y
            res_8b = self.fh.getActualNum(oper)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.x = res_8b

        def zpy_stx(self, Y):
            addr = self.decoder.immediate + self.cpu.y
            self.cpu.mem_bus.write(addr, self.cpu.x)
