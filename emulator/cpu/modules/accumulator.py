from cpu.modules.flag_handler import FlagHandler

class Accumulator():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    def acc_asl(self):
        pass

    def acc_lsr(self):
        pass

    def acc_rol(self):
        pass

    def acc_ror(self):
        pass
