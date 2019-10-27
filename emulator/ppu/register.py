class Register:

    def __init__(self):
        self.size = self.getSize()
        self.mod = 2**self.size
        self.data = 0

    def load(self):
        return self.data % self.mod

    def loadBit(self, pos):
        return (self.data >> pos) & 1

    # Load "offset" number of bits, starting from "start"
    def loadBits(self, start, offset):
        mask = ((self.mod - 1) >> start) % (1 << offset)
        return ((self.data >> start) & mask) % self.mod

    def store(self, value):
        self.data = value % self.mod

    def storeBit(self, pos, value):
        # erase bit
        self.data = self.data - ((self.data >> pos) & 1) * (1 << pos)
        self.data = (self.data + ((value & 1) << pos)) % self.mod

    def storeBits(self, start, offset, value):
        mask = ((1 << offset) - 1) << (start)
        #mask = (((self.mod - 1) >> start) % (1 << (offset+1))) << start
        # erase bits
        self.data = (self.data & ~mask) % self.mod
        self.data = (self.data + ((value << start) & mask)) % self.mod

    def clear(self):
        self.data = 0

    def clearBit(self, pos):
        self.storeBit(pos, 0)

    def isBitSet(self, pos):
        return self.loadBit(pos) == 1

    def increment(self):
        self.data = (self.data + 1) % self.mod

    def add(self, value):
        self.data = (self.data + value) % self.mod

    def decrement(self):
        self.data = (self.data - 1) % self.mod

    def sub(self, value):
        self.data = (self.data - value) % self.mod

    def shift(self, carry_in):
        carry_out = self.loadBit(self.size - 1)
        self.data = ((self.data << 1) + (carry_in & 1)) % self.mod
        return carry_out

class Register8Bit(Register):

    def getSize(self):
        return 8


class Register16Bit(Register):

    def getSize(self):
        return 16

    def loadHigherByte(self):
        return self.loadBits(8, 8)

    def loadLowerByte(self):
        return self.loadBits(0, 8)

    def storeHigherByte(self, value):
        self.storeBits(8, 8, value)

    def storeLowerByte(self, value, deb=False):
        self.storeBits(0, 8, value)
