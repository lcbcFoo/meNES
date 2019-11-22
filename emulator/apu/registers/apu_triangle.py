class APUTRIANGLE:
    def __init__(self, apu):
        self.apu = apu
        # self.reg = register
        self.reset()

    def reset(self):
        #self.reg.store(0)
        self.sequence = [15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0,\
 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15]
        self.reload = 0x0000
        self.timer = 0x0000
        self.pos = 0
        self.output = 0x00
        self.enable = False

        self.frequency = 0
        self.dutycycle = 0
        self.amplitude = 128
        self.pi = 3.14159
        self.harmonics = 20

    def clock(self, pulse_enable):
        if(pulse_enable):
            self.timer-=1
            if(self.timer == -1):
                self.timer = self.reload + 1
                sample = self.sequence[self.pos]
                self.pos += 1
                if self.pos == len(self.sequence):
                    self.pos = 0

                self.output = sample

        return self.output
