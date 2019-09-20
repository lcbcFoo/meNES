from cpu.modules.decoder import Decoder
from cpu.modules.flag_handler import FlagHandler

class Absolute():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.handler = self.cpu.flag_handler

    def abs_adc(self):
        absolute = self.decoder.content
        result = self.cpu.a + absolute + self.cpu.c
        actualResult = self.decoder.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetCarry(actualResult)
        self.handler.SetOverflow(self.cpu.a, absolute, actualResult)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    def abs_and(self):
        oper = self.decoder.content
        result = self.cpu.a & oper
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def abs_asl(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = oper << 1
        result = self.handler.getActualNum(result)
        self.cpu.mem_bus.write(oper_addr, result, n=1)
        self.handler.SetNegative(result)
        self.handler.SetZero(result)
        self.handler.SetCarry(result)

    # def abs_bit(self):
    #     oper = self.decoder.content
    #     oper_addr = self.decoder.full_addr
    #     result = oper & self.cpu.a
    #     pass

    def abs_cmp(self):
        oper = self.decoder.content
        result = self.cpu.a - oper
        actualResult = self.handler.getActualNum(result)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetCarry(actualResult)

    def abs_cpx(self):
        oper = self.decoder.content
        result = self.cpu.x - oper
        actualResult = self.handler.getActualNum(result)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetCarry(actualResult)

    def abs_cpy(self):
        oper = self.decoder.content
        result = self.cpu.y - oper
        actualResult = self.handler.getActualNum(result)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetCarry(actualResult)

    def abs_dec(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = self.handler.getActualNum(oper-1)
        self.cpu.mem_bus.write(oper_addr, result, n=1)

    def abs_eor(self):
        oper = self.decoder.content
        result = self.cpu.a ^ oper
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    def abs_inc(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = self.handler.getActualNum(oper+1)
        self.cpu.mem_bus.write(oper_addr, result, n=1)
    
    # Probably is incomplete since doesn't check page
    # def abs_jmp(self):
    #     oper = self.decoder.content
    #     self.cpu.pc = oper
    #     pass

    # def abs_jsr(self):
    #     oper = self.decoder.content
    #     pass

    def abs_lda(self):
        oper = self.decoder.content
        result = self.handler.getActualNum(oper)
        self.cpu.a = result
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def abs_ldx(self):
        oper = self.decoder.content
        result = self.handler.getActualNum(oper)
        self.cpu.x = result
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def abs_ldy(self):
        oper = self.decoder.content
        result = self.handler.getActualNum(oper)
        self.cpu.y = result
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def abs_lsr(self):
        oper = self.decoder.content
        oper_addr = self.decoder.full_addr
        result = oper >> 1
        result = self.handler.getActualNum(result)
        self.cpu.mem_bus.write(oper_addr, result, n=1)
        self.handler.SetNegative(result)
        self.handler.SetZero(result)
        self.handler.SetCarry(result)

    def abs_ora(self):
        oper = self.decoder.content
        result = self.cpu.a | oper
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    # def abs_rol(self):
    #     oper = self.decoder.content
    #     oper_addr = self.decoder.full_addr
    #     result = oper << 1
    #     result = self.handler.getActualNum(result)
    #     self.handler.SetNegative(result)
    #     self.handler.SetZero(result)
    #     self.handler.SetCarry(result)

    #     # Sets bit 0 to carry bit
    #     if self.cpu.c & 1 == 1:
    #         result = result | 1

    #     # Sets carry bit to bit 7
        
    #     self.cpu.mem_bus.write(oper_addr, result, n=1)

    # def abs_ror(self):
    #     oper = self.decoder.content
    #     oper_addr = self.decoder.full_addr
    #     new_carry = oper & 1 == 1 # Gets carry bit info
    #     new_bit_7 = self.cpu.c
    #     result = oper >> 1
    #     result = new_bit_7 <
    #     result = self.handler.getActualNum(result)
    #     self.handler.SetNegative(result)
    #     self.handler.SetZero(result)
    #     self.handler.SetCarry(result)

    #     # Sets carry bit to bit 7
    #     if new_carry:
    #         self.cpu.c = 1
    #     else:
    #         self.cpu.c = 0

    #     # Set bit 0 to carry bit
        
    #     self.cpu.mem_bus.write(oper_addr, result, n=1)

    def abs_sbc(self):
        oper = self.decoder.content
        result = self.cpu.a - oper - self.cpu.c
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetOverflow(actualResult)
        self.handler.SetCarry(actualResult)

    def abs_sta(self):
        oper = self.decoder.content
        address = self.handler.getActualNum(oper)
        self.cpu.mem_bus.write(address, self.cpu.a, n=1)

    def abs_stx(self):
        oper = self.decoder.content
        address = self.handler.getActualNum(oper)
        self.cpu.mem_bus.write(address, self.cpu.x, n=1)

    def abs_sty(self):
        oper = self.decoder.content
        address = self.handler.getActualNum(oper)
        self.cpu.mem_bus.write(address, self.cpu.y, n=1)

    ###################################################################################################################
    ############### ABSOLUTE X OPERATIONS #############################################################################
    
    def absX_adc(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a + absolute_x + self.cpu.c
        actualResult = self.decoder.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetCarry(actualResult)
        self.handler.SetOverflow(self.cpu.a, absolute_x, actualResult)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    def absX_and(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a & absolute_x
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def absX_asl(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr
        result = absolute_x << 1
        result = self.handler.getActualNum(result)
        self.cpu.mem_bus.write(oper_addr, result, n=1)
        self.handler.SetNegative(result)
        self.handler.SetZero(result)
        self.handler.SetCarry(result)

    def absX_cmp(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a - absolute_x
        actualResult = self.handler.getActualNum(result)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetCarry(actualResult)

    def absX_dec(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr
        result = self.handler.getActualNum(absolute_x-1)
        self.cpu.mem_bus.write(oper_addr, result, n=1)


    def absX_eor(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a ^ absolute_x
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    def absX_inc(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr
        result = self.handler.getActualNum(absolute_x+1)
        self.cpu.mem_bus.write(oper_addr, result, n=1)


    def absX_lda(self):
        absolute_x = self.decoder.content_x
        result = self.handler.getActualNum(absolute_x)
        self.cpu.a = result
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def absX_ldy(self):
        absolute_x = self.decoder.content_x
        result = self.handler.getActualNum(absolute_x)
        self.cpu.y = result
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def absX_lsr(self):
        absolute_x = self.decoder.content_x
        oper_addr = self.decoder.full_addr
        result = absolute_x >> 1
        result = self.handler.getActualNum(result)
        self.cpu.mem_bus.write(oper_addr, result, n=1)
        self.handler.SetNegative(result)
        self.handler.SetZero(result)
        self.handler.SetCarry(result)

    def absX_ora(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a | absolute_x
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    # def absX_rol(self):
    #     pass

    # def absX_ror(self):
    #     pass

    def absX_sbc(self):
        absolute_x = self.decoder.content_x
        result = self.cpu.a - absolute_x - self.cpu.c
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetOverflow(actualResult)
        self.handler.SetCarry(actualResult)

    def absX_sta(self):
        absolute_x = self.decoder.content_x
        address = self.handler.getActualNum(absolute_x)
        self.cpu.mem_bus.write(address, self.cpu.a, n=1)



    ###################################################################################################################
    ############### ABSOLUTE Y OPERATIONS #############################################################################
    ###################################################################################################################

    def absY_adc(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a + absolute_y + self.cpu.c
        actualResult = self.decoder.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetCarry(actualResult)
        self.handler.SetOverflow(self.cpu.a, absolute_y, actualResult)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    def absY_and(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a & absolute_y
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def absY_cmp(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a - absolute_y
        actualResult = self.handler.getActualNum(result)
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetCarry(actualResult)

    def absY_eor(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a ^ absolute_y
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    def absY_lda(self):
        absolute_y = self.decoder.content_y
        result = self.handler.getActualNum(absolute_y)
        self.cpu.a = result
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def absY_ldx(self):
        absolute_y = self.decoder.content_y
        result = self.handler.getActualNum(absolute_y)
        self.cpu.x = result
        self.handler.SetNegative(result)
        self.handler.SetZero(result)

    def absY_ora(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a | absolute_y
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)

    def absY_sbc(self):
        absolute_y = self.decoder.content_y
        result = self.cpu.a - absolute_y - self.cpu.c
        actualResult = self.handler.getActualNum(result)
        self.cpu.a = actualResult
        self.handler.SetNegative(actualResult)
        self.handler.SetZero(actualResult)
        self.handler.SetOverflow(actualResult)
        self.handler.SetCarry(actualResult)

    def absY_sta(self):
        absolute_y = self.decoder.content_y
        address = self.handler.getActualNum(absolute_y)
        self.cpu.mem_bus.write(address, self.cpu.a, n=1)
