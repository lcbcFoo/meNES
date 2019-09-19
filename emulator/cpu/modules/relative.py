from cpu.modules.flag_handler import FlagHandler

class Relative():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    def rel_bpl(self):
        pass

    def rel_bmi(self):
        pass

    def rel_bvc(self):
        pass

    def rel_bvs(self):
        pass

    def rel_bcc(self):
        pass

    def rel_bcs(self):
        pass

    def rel_bne(self):
        pass

    def rel_beq(self):
        pass
