from apu.square_wave import SquareWave
from apu.registers.apu_pulse import APUPULSE
from apu.registers.apu_triangle import APUTRIANGLE
import numpy as np

class APU:
    def __init__(self, gui):
        self.sqwave = SquareWave()
        self.gui = gui
        self.time = 0
        self.pulse1 = APUPULSE(self)
        self.pulse1_enable = False
        self.pulse1_sample = 0.0
        self.pulse2 = APUPULSE(self)
        self.pulse2_enable = False
        self.pulse2_sample = 0.0
        self.triangle = APUTRIANGLE(self)
        self.triangle_enable = False
        self.triangle_sample = False
        self.clock_counter = 0
        self.frame_clock_counter = 0
        self.audioTime = 0
        self.audioTimeperNesClock = 0
        self.audioTimeperSystemSample = 0
        self.sndarray = [0]*44100
        self.sndarray = (np.asarray(self.sndarray, dtype=np.int16))

    def register_write(self, addr, data):
        if(addr <= 0x4003):
            self.pulse1.write(data, addr)
        elif(addr <= 0x4007):
            self.pulse2.write(data, addr)
        if(addr == 0x4015):
            # print("Sound enable")
            self.pulse1_enable = data & 0x01;
            self.pulse2_enable = data & 0x02;
            self.triangle_enable = data & 0x03;


    def run(self):

        quarterFrameClock = False
        halfFrameClock = False

        self.time += (0.333333333/1789773)
        if(self.clock_counter % 6 == 0):
            self.frame_clock_counter += 1

            if self.frame_clock_counter == 3729:
                quarterFrameClock = True

            if self.frame_clock_counter == 7457:
                quarterFrameClock = True
                halfFrameClock = True

            if self.frame_clock_counter == 11186:
                quarterFrameClock = True

            if self.frame_clock_counter == 14916:
                quarterFrameClock = True
                halfFrameClock = True
                self.frame_clock_counter = 0

            #TODO
            if quarterFrameClock:
                pass

            #TODO
            if halfFrameClock:
                pass

            # self.pulse1_sample = self.pulse1.clock(self.pulse1_enable)
            self.pulse1_sample = self.pulse1.sample(self.time)
            self.pulse2_sample = self.pulse2.sample(self.time)
            self.triangle_sample = self.triangle.clock(self.triangle_enable)

            self.output = ((self.pulse1_enable & 1)*self.pulse1_sample) + ((self.pulse2_enable & 1) * self.pulse2_sample)  + ((self.triangle_enable & 1) * self.triangle_sample)

        self.clock_counter += 1

        if((self.clock_counter % 44100 == 0)):
            # self.sndarray[44099] = self.pulse1_sample*180 + 38
            self.sndarray[44099] = self.output
            self.gui.play_sound(self.sndarray)
        else:
            # self.sndarray[self.clock_counter % 44100 - 1] = self.pulse1_sample*180 + 38
            self.sndarray[self.clock_counter % 44100 - 1] = self.output

        # step = 1/44100
        # self.sqwave.changeHarmonic(value)
        # array = [0]*44100
        # array = (np.asarray(array, dtype=np.int16))
        # while(self.time < 1):
        #     for i in range(44100):
        #         array[i] = (self.sqwave.sampleSinWave(1000, self.time))
        #         self.time += step
        #     print(self.time)
        #     #self.gui.stop_sound()
        #     self.gui.play_sound(array)
        # self.time = 0

    def getOutputSample(self):
        return self.pulse1_sample;
