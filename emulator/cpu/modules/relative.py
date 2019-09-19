from cpu.modules.flag_handler import FlagHandler

class Relative():
    def __init__(self, cpu, mem, decoder):
        self.cpu = cpu
        self.mem = mem
        self.decoder = decoder
        self.fh = FlagHandler(cpu)

    def branch(self):
        npc = self.cpu.pc
        imm = self.decoder.immediate

        if imm >= 0x80:
            npc = npc + (~imm + 1)
        else:
            npc = npc + imm
        
        self.cpu.pc = npc
        self.cpu.update_pc = False

    def rel_bpl(self):
        if self.cpu.n == 0:
            self.branch()

    def rel_bmi(self):
        if self.cpu.n == 1:
            self.branch()

    def rel_bvc(self):
        if self.cpu.v == 0:
            self.branch()

    def rel_bvs(self):
        if self.cpu.v == 1:
            self.branch()

    def rel_bcc(self):
        if self.cpu.c == 0:
            self.branch()

    def rel_bcs(self):
        if self.cpu.c == 1:
            self.branch()

    def rel_bne(self):
        if self.cpu.z == 0:
            self.branch()

    def rel_beq(self):
        if self.cpu.z == 1:
            self.branch()
