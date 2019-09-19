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

    def imp_clc(self):
        self.cpu.c=0

    def imp_sec(self):
        self.cpu.c=1

    def imp_cli(self):
        self.cpu.i=0

    def imp_sei(self):
        self.cpu.i=1

    def imp_clv(self):
        self.cpu.v=0

    def imp_cld(self):
        self.cpu.d=0

    def imp_sed(self):
        self.cpu.d=1


    def imp_txs(self):
        pass
    def imp_tsx(self):
        pass
    def imp_pha(self):
        pass
    def imp_pla(self):
        pass
    def imp_php(self):
        pass
    def imp_plp(self):
        pass

    def imp_tax(self):
        self.cpu.x = self.cpu.a
        self.fh.setNegative(self.cpu.x)
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
