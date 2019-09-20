from cpu.modules.flag_handler import FlagHandler

class Implied():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    def imp_brk(self):
        pass
    def imp_nop(self):
        pass
    def imp_rti(self):
        pass
    def imp_rts(self):
        pass

    # Flag modify functions
    # Clear the carry flag
    def imp_clc(self):
        self.cpu.c=0

    # Set carry flag to 1
    def imp_sec(self):
        self.cpu.c=1

    # Clear interrupt flag
    def imp_cli(self):
        self.cpu.i=0

    # Set interrupt flag to 1
    def imp_sei(self):
        self.cpu.i=1

    # Clear overflow flag
    def imp_clv(self): #Not tested yet
        self.cpu.v=0

    # Clear decimal flag
    def imp_cld(self):
        self.cpu.d=0

    # Set decimal flag 1
    def imp_sed(self):
        self.cpu.d=1


    # Stack functions
    # Transfer value from reg_x to the stack point
    def imp_txs(self):
        self.cpu.sp = self.cpu.x

    # Transfer the low
    def imp_tsx(self):
        self.cpu.x = self.cpu.sp
        self.fh.setNegative(self.cpu.x)
        self.fh.setZero(self.cpu.x)

    def imp_pha(self):
        stack_addr = 0x01<<8 + self.cpu.sp
        self.mem.write(stack_addr, self.cpu.a)
        self.cpu.sp -= 1

    def imp_pla(self):
        self.cpu.sp += 1
        self.cpu.a = self.mem.read(self.cpu.sp)
        self.fh.setNegative(self.cpu.a)
        self.fh.setZero(self.cpu.a)

    def imp_php(self):
        self.mem.write(self.cpu.sp, self.cpu.n)
        self.cpu.sp -= 1
        self.mem.write(self.cpu.sp, self.cpu.v)
        self.cpu.sp -= 1
        self.mem.write(self.cpu.sp, self.cpu.b)
        self.cpu.sp -= 1
        self.mem.write(self.cpu.sp, self.cpu.d)
        self.cpu.sp -= 1
        self.mem.write(self.cpu.sp, self.cpu.i)
        self.cpu.sp -= 1
        self.mem.write(self.cpu.sp, self.cpu.z)
        self.cpu.sp -= 1
        self.mem.write(self.cpu.sp, self.cpu.c)
        self.cpu.sp -= 1

    def imp_plp(self):
        self.cpu.sp += 1
        self.cpu.c = self.mem.read(self.cpu.sp)
        self.cpu.sp += 1
        self.cpu.z = self.mem.read(self.cpu.sp)
        self.cpu.sp += 1
        self.cpu.i = self.mem.read(self.cpu.sp)
        self.cpu.sp += 1
        self.cpu.d = self.mem.read(self.cpu.sp)
        self.cpu.sp += 1
        self.cpu.b = self.mem.read(self.cpu.sp)
        self.cpu.sp += 1
        self.cpu.v = self.mem.read(self.cpu.sp)
        self.cpu.sp += 1
        self.cpu.n = self.mem.read(self.cpu.sp)

    #Index registers functions
    def imp_tax(self):
        self.cpu.x = self.cpu.a
        self.fh.setNegative(self.cpu.x) #not Tested yet
        self.fh.setZero(self.cpu.x)

    def imp_txa(self):
        self.cpu.a = self.cpu.x
        self.fh.setNegative(self.cpu.a)
        self.fh.setZero(self.cpu.a)

    def imp_dex(self):
        self.cpu.x -= 1
        self.fh.setNegative(self.cpu.x)
        self.fh.setZero(self.cpu.x)

    def imp_inx(self):
        self.cpu.x += 1
        self.fh.setNegative(self.cpu.x)
        self.fh.setZero(self.cpu.x)

    def imp_tay(self):
        self.cpu.y = self.cpu.a
        self.fh.setNegative(self.cpu.y)
        self.fh.setZero(self.cpu.y)

    def imp_tya(self):
        self.cpu.a = self.cpu.y
        self.fh.setNegative(self.cpu.a)
        self.fh.setZero(self.cpu.a)

    def imp_dey(self):
        self.cpu.y -= 1
        self.fh.setNegative(self.cpu.y)
        self.fh.setZero(self.cpu.y)

    def imp_iny(self):
        self.cpu.y += 1
        self.fh.setNegative(self.cpu.y)
        self.fh.setZero(self.cpu.y)
