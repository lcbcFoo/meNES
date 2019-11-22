def approxsin(t):
    j = t*0.15915
    j = j - int(j)
    return 20.785*j*(j-0.5)*(j-1)

class APUPULSE:

    def __init__(self, apu):
        self.apu = apu
        # self.reg = register
        self.reset()

    def reset(self):
        #self.reg.store(0)
        self.sequence = 0x00000000
        self.reload = 0x0000
        self.timer = 0x0000
        self.output = 0x00

        self.frequency = 0
        self.dutycycle = 0
        self.amplitude = 128
        self.pi = 3.14159
        self.harmonics = 20

    def read(self):
        return self.reg.load()

    def write(self,value, addr):
        if(addr == 0x4000):
            if((value & 0xC0) >> 6) == 0x00:
                self.sequence = 0b00000001
                self.dutycycle = 0.125
            elif((value & 0xC0) >> 6) == 0x01:
                self.sequence = 0b00000011
                self.dutycycle = 0.250
            elif((value & 0xC0) >> 6) == 0x02:
                self.sequence = 0b00001111
                self.dutycycle = 0.500
            elif((value & 0xC0) >> 6) == 0x03:
                self.sequence = 0b11111100
                self.dutycycle = 0.750

        elif(addr == 0x4002):
            self.reload = self.reload & 0xFF00 | value

        elif(addr == 0x4003):
            self.reload = value & 0x07 << 8 | self.reload & 0x00FF
            self.timer = self.reload

        #self.reg.store(value)

    def clock(self, pulse_enable):
        if(pulse_enable):
            self.timer-=1
            if(self.timer == -1):
                self.timer = self.reload + 1
                self.sequence = ((self.sequence & 0x0001) << 7) | ((self.sequence & 0x00FE) >> 1)
                self.output = self.sequence & 0x00000001

        return self.output

    def sample(self, time):
        a = 0.0
        b = 0.0
        p = self.dutycycle * 2 * self.pi

        self.frequency = 1789773.0/(16.0*(self.reload+1))

        for n in range(1, self.harmonics):
            c = n*self.frequency*2*self.pi*time;
            a += -approxsin(c) / n;
            b += -approxsin(c-p*n)/n;

        return int(128 + 25*(2/self.pi) * (a-b))
