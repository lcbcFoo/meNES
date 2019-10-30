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
            npc = npc - ((~(imm - 1))%256)
        else:
            npc = npc + imm

        # Adds additional cycle if page boundary was crossed
        self.cpu.additional_cycle = self.cpu.set_additional_cycle(npc)
        # Adds additional cycle since branch was taken
        self.cpu.additional_cycle += 1
        self.cpu.pc = npc

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
