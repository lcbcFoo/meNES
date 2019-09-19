from cpu.modules.flag_handler import FlagHandler

class ZeroPage():

        def __init__(self, cpu, mem, decoder):
            self.cpu = cpu
            self.mem = mem
            self.decoder = decoder
            self.fh = FlagHandler(cpu)

        def zp_adc(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + oper + carry
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setOverflow(reg_a, oper, res_8b)
            self.setNegative(res_8b)
            self.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_and(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a & oper
            res_8b = self.fh.getActualNum(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_asl(self):
            oper = self.decoder.cont_zp
            res = oper << 1
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setNegative(res_8b)
            self.fh.setZero(res_8b)
            self.cpu.a = res_8b

        def zp_bit(self):
            pass

        def zp_cmp(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a - oper
            res_8b = self.fh.getActualNum(res)
            self.fh.SetCarry(res)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)

        def zp_cpx(self):
            oper = self.decoder.cont_zp
            reg_x = self.cpu.x
            res = reg_x - oper
            res_8b = self.fh.getActualNum(res)
            self.fh.SetCarry(res)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)

        def zp_cpy(self):
            oper = self.decoder.cont_zp
            reg_y = self.cpu.y
            res = reg_y - oper
            res_8b = self.fh.getActualNum(res)
            self.fh.SetCarry(res)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)

        def zp_dec(self):
            pass

        def zp_eor(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a ^ oper
            res_8b = self.fh.getActualNum(res)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)
            self.cpu.a = res_8b

        def zp_inc(self):
            pass

        def zp_lda(self):
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)
            self.cpu.a = res_8b

        def zp_ldx(self):
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)
            self.cpu.x = res_8b

        def zp_ldy(self):
            oper = self.decoder.cont_zp
            res_8b = self.fh.getActualNum(oper)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)
            self.cpu.y = res_8b

        def zp_lsr(self):
            pass

        def zp_ora(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            res = reg_a | oper
            res_8b = self.fh.getActualNum(res)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)
            self.cpu.a = res_8b

        def zp_rol(self):
            pass

        def zp_ror(self):
            pass

        def zp_sbc(self):
            oper = self.decoder.cont_zp
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + ~immediate + ~carry
            res_8b = self.fh.getActualNum(res)
            self.fh.SetCarry(res)
            self.fh.SetOverflow(reg_a, oper, res_8b)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)
            self.cpu.a = res_8b

        def zp_sta(self):
            pass

        def zp_stx(self):
            pass

        def zp_sty(self):
            pass

        def zpx_adc(self, X):
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            carry = self.cpu.c
            res = reg_a + oper + carry
            res_8b = self.fh.getActualNum(res)
            self.fh.setCarry(res)
            self.fh.setOverflow(reg_a, oper, res_8b)
            self.setNegative(res_8b)
            self.setZero(res_8b)
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
            self.fh.SetCarry(res)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)

        def zpx_dec(self, X):
            pass

        def zpx_eor(self, X):
            oper = self.decoder.cont_zp_x
            reg_a = self.cpu.a
            res = reg_a ^ oper
            res_8b = self.fh.getActualNum(res)
            self.fh.SetNegative(res_8b)
            self.fh.SetZero(res_8b)
            self.cpu.a = res_8b

        def zpx_inc(self, X):
            pass

        def zpx_lda(self, X):
            pass

        def zpx_ldy(self, X):
            pass

        def zpx_lsr(self, X):
            pass

        def zpx_ora(self, X):
            pass

        def zpx_rol(self, X):
            pass

        def zpx_ror(self, X):
            pass

        def zpx_sbc(self, X):
            pass

        def zpx_sta(self, X):
            pass

        def zpx_sty(self, X):
            pass

        def zpy_ldx(self, Y):
            pass

        def zpy_stx(self, Y):
            pass
