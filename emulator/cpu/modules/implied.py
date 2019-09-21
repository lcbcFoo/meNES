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

    # Transfer the value from stack pointer to reg_x
    # Flags: N, Z (from reg_x).
    def imp_tsx(self):
        self.cpu.x = self.cpu.sp
        self.fh.setNegative(self.cpu.x)
        self.fh.setZero(self.cpu.x)

    # Push the value from reg_a to the stack.
    # Then decrements stack pointer by 1.
    def imp_pha(self):
        stack_addr = 0x0100 + self.cpu.sp
        self.mem.write(stack_addr, self.cpu.a)
        self.cpu.sp -= 1

    # Increments stack pointer by 1. Then pull the first value from the stack to
    # reg_a.
    # Flags: N, Z (from reg_a).
    def imp_pla(self):
        self.cpu.sp += 1
        stack_addr = 0x0100 + self.cpu.sp
        self.cpu.a = self.mem.read(stack_addr)
        self.fh.setNegative(self.cpu.a)
        self.fh.setZero(self.cpu.a)

    # Add all the flags to an 8bit register like follows : NV-BDIZC
    # Then push this register to the stack. Then decrements stack pointer by 1.
    def imp_php(self):
        status_reg = 0
        status_reg += (self.cpu.n << 7)
        status_reg += (self.cpu.v << 6)
        status_reg += (self.cpu.b << 4)
        status_reg += (self.cpu.d << 3)
        status_reg += (self.cpu.i << 2)
        status_reg += (self.cpu.z << 1)
        status_reg += self.cpu.c

        stack_addr = 0x0100 + self.cpu.sp
        self.mem.write(stack_addr, status_reg)
        self.cpu.sp -= 1

    # Increments the stack pointer by 1. Then pull the first value from the
    # stack to status_reg (NV-BDIZC).
    # Then save each bit of the status_reg to the respective flag.
    def imp_plp(self):
        self.cpu.sp += 1
        stack_addr = 0x0100 + self.cpu.sp
        status_reg = self.mem.read(self.cpu.sp)
        self.cpu.c = status_reg & (0x01 << 0 )
        self.cpu.z = status_reg & (0x01 << 1 )
        self.cpu.i = status_reg & (0x01 << 2 )
        self.cpu.d = status_reg & (0x01 << 3 )
        self.cpu.b = status_reg & (0x01 << 4 )
        self.cpu.v = status_reg & (0x01 << 6 )
        self.cpu.n = status_reg & (0x01 << 7 )

    # Index registers functions
    # Transfer value from reg_a to reg_x.
    # Flags: N, Z (from reg_x).
    def imp_tax(self):
        self.cpu.x = self.cpu.a
        self.fh.setNegative(self.cpu.x) #not Tested yet
        self.fh.setZero(self.cpu.x)

    # Transfer value from reg_x to reg_a.
    # Flags: N, Z (from reg_a).
    def imp_txa(self):
        self.cpu.a = self.cpu.x
        self.fh.setNegative(self.cpu.a)
        self.fh.setZero(self.cpu.a)

    # Decrements reg_x by 1.
    # Flags: N, Z (from reg_x).
    def imp_dex(self):
        self.cpu.x -= 1
        self.fh.setNegative(self.cpu.x)
        self.fh.setZero(self.cpu.x)

    # Increments reg_x by 1.
    # Flags: N, Z (from reg_x).
    def imp_inx(self):
        self.cpu.x += 1
        self.fh.setNegative(self.cpu.x)
        self.fh.setZero(self.cpu.x)

    # Transfer value from reg_a to reg_y.
    # Flags: N, Z (from reg_y).
    def imp_tay(self):
        self.cpu.y = self.cpu.a
        self.fh.setNegative(self.cpu.y)
        self.fh.setZero(self.cpu.y)

    # Transfer value from reg_y to reg_a.
    # Flags: N, Z (from reg_a).
    def imp_tya(self):
        self.cpu.a = self.cpu.y
        self.fh.setNegative(self.cpu.a)
        self.fh.setZero(self.cpu.a)

    # Decrements reg_y by 1.
    # Flags: N, Z (from reg_y).
    def imp_dey(self):
        self.cpu.y -= 1
        self.fh.setNegative(self.cpu.y)
        self.fh.setZero(self.cpu.y)

    # Increments reg_y by 1.
    # Flags: N, Z (from reg_y).
    def imp_iny(self):
        self.cpu.y += 1
        self.fh.setNegative(self.cpu.y)
        self.fh.setZero(self.cpu.y)
