from decoder import *
from flag_handler import *

class Absolute():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder

    def abs_adc(self):
        absolute = decoder.content
        result = self.cpu.a + absolute + self.cpu.c
        actualResult = self.decoder.getActualNum(result)
        self.cpu.a = actualResult
        self.decoder.SetCarry(actualResult)
        self.decoder.SetOverflow(self.cpu.a, self.abs, actualResult)
        self.decoder.SetNegative(actualResult)
        self.decoder.SetZero(actualResult)

    def abs_and(self, oper):
        pass

    def abs_asl(self, oper):
        pass

    def abs_bit(self, oper):
        pass

    def abs_cmp(self, oper):
        pass

    def abs_cpx(self, oper):
        pass

    def abs_cpy(self, oper):
        pass

    def abs_dec(self, oper):
        pass

    def abs_eor(self, oper):
        pass

    def abs_inc(self, oper):
        pass

    def abs_jmp(self, oper):
        pass

    def abs_jsr(self, oper):
        pass

    def abs_lda(self, oper):
        pass

    def abs_ldx(self, oper):
        pass

    def abs_ldy(self, oper):
        pass

    def abs_lsr(self, oper):
        pass

    def abs_ora(self, oper):
        pass

    def abs_rol(self, oper):
        pass

    def abs_ror(self, oper):
        pass

    def abs_sbc(self, oper):
        pass

    def abs_sta(self, oper):
        pass

    def abs_stx(self, oper):
        pass

    def abs_sty(self, oper):
        pass

    ###################################################################################################################
    ############### ABSOLUTE X OPERATIONS #############################################################################
    
    def absX_adc(self, oper, X):
        pass

    def absX_and(self, oper, X):
        pass

    def absX_asl(self, oper, X):
        pass

    def absX_cmp(self, oper, X):
        pass

    def absX_dec(self, oper, X):
        pass

    def absX_eor(self, oper, X):
        pass

    def absX_inc(self, oper, X):
        pass

    def absX_lda(self, oper, X):
        pass

    def absX_ldy(self, oper, X):
        pass

    def absX_lsr(self, oper, X):
        pass

    def absX_ora(self, oper, X):
        pass

    def absX_rol(self, oper, X):
        pass

    def absX_ror(self, oper, X):
        pass

    def absX_sbc(self, oper, X):
        pass

    def absX_sta(self, oper, X):
        pass


    ###################################################################################################################
    ############### ABSOLUTE Y OPERATIONS #############################################################################
    ###################################################################################################################

    def absY_adc(self, oper, Y):
        pass

    def absY_and(self, oper, Y):
        pass

    def absY_cmp(self, oper, Y):
        pass

    def absY_eor(self, oper, Y):
        pass

    def absY_lda(self, oper, Y):
        pass

    def absY_ldx(self, oper, Y):
        pass

    def absY_ora(self, oper, Y):
        pass

    def absY_sbc(self, oper, Y):
        pass

    def absY_sta(self, oper, Y):
        pass
