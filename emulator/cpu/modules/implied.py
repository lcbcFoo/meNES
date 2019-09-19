from cpu.modules.flag_handler import FlagHandler

class Implied():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    def imp_brk(self, oper):
        pass
    def imp_nop(self, oper):
        pass
    def imp_rti(self, oper):
        pass
    def imp_rts(self, oper):
        pass

    def imp_clc(self, oper):
        pass
    def imp_sec(self, oper):
        pass
    def imp_cli(self, oper):
        pass
    def imp_sei(self, oper):
        pass
    def imp_clv(self, oper):
        pass
    def imp_cld(self, oper):
        pass
    def imp_sed(self, oper):
        pass

    def imp_txs(self, oper):
        pass
    def imp_tsx(self, oper):
        pass
    def imp_pha(self, oper):
        pass
    def imp_pla(self, oper):
        pass
    def imp_php(self, oper):
        pass
    def imp_plp(self, oper):
        pass

    def imp_tax(self, oper):
        pass
    def imp_txa(self, oper):
        pass
    def imp_dex(self, oper):
        pass
    def imp_inx(self, oper):
        pass
    def imp_tay(self, oper):
        pass
    def imp_tya(self, oper):
        pass
    def imp_dey(self, oper):
        pass
    def imp_iny(self, oper):
        pass
