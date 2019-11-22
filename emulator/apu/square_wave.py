import sys
import pygame
import time
import numpy as np
import math

def approxsin(t):
    j = t*0.15915
    j = j - int(j)
    return 20.785*j*(j-0.5)*(j-1)

def sine_array_onecycle(hz, peak):
    length = 44100 / float(hz)
    omega = np.pi * 2 * length
    xvalues = np.arange(int(length)) * omega
    return (np.sin(xvalues)).astype(np.float32)

def sine_array(hz, peak, n_samples = 44100):
    array = sine_array_onecycle(hz, peak)
    return np.resize(array, (n_samples,))

class SquareWave():

    def __init__(self):
        self.nHarmonics = 20

    def changeHarmonic(self, value):
        self.nHarmonics = value

    def sampleSquareWave(self, f, t):
        a = 0.0
        b = 0.0
        p = 0.5 * 2 * np.pi

        for n in range(1, self.nHarmonics):
            c = n*f*2*np.pi*t;
            a += approxsin(c) / n;
            b += approxsin(c-p*n)/n;

        return int(128 + 25*(2/np.pi) * (a-b))

    def createFullWave(self, f):
        array = [0] * 44100

        for i in range(44100):
            array[i] = self.sampleSquareWave(f, i*1/44100)
        #omega = np.pi * 2 * length
        #xvalues = np.arange(int(length)) * omega
        array = (np.asarray(array, dtype=np.int16))
        return array

    def sampleSinWave(self, f, t):
        c = f*2*np.pi*t;
        return int(128 + 90*(math.sin(c)));
