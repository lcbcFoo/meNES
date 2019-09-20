from cpu.modules.flag_handler import FlagHandler

class Indirect():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    def ind_jmp(self):
        pass


    def indx_adc(self):
        pass

    def indx_and(self):
        pass

    def indx_cmp(self):
        pass

    def indx_eor(self):
        pass

    def indx_lda(self):
        pass

    def indx_ora(self):
        pass

    def indx_sbc(self):
        pass

    def indx_sta(self):
        pass


    def indy_adc(self):
        pass

    def indy_and(self):
        pass

    def indy_cmp(self):
        pass

    def indy_eor(self):
        pass

    def indy_lda(self):
        pass

    def indy_ora(self):
        pass

    def indy_sbc(self):
        pass

    def indy_sta(self):
        pass
