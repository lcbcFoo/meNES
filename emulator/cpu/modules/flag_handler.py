MAX_NUM = 127
MIN_NUM = -128

# NOTATION
# res1: represents the result of an operation in decimal values. Could be any
#       number. (> MAX_NUM or < MIN_NUM)
# res2: represents the same result as a two's complement of an 8-bit number.
#
# Before using any methods with parameter called "res2", first call the method
# getActualNum() to convert res1 into an res2 format number.

class FlagHandler():

    def __init__(self, cpu):
        self.cpu = cpu

    # Transforms a number into the a two's complement 8-bit number that fits
    # inside the register.
    # Example: 128 -> -128      (in decimal)
    #          224 -> -32
    #          -130 -> 126
    #          -242 -> 14
    def getActualNum(self, res1):
        if res1 > MAX_NUM:
            res2 = (res1 % (MAX_NUM + 1)) - (MAX_NUM + 1)
        elif res1 < MIN_NUM:
            res2 = res1 % (MAX_NUM + 1)
        else:
            res2 = res1
        return res2

    # If the result of an operation is bigger than MAX_NUM or smaller than
    # MIN_NUM, sets the Carry Flag to 1.
    def SetCarry(self, res1):
        if res1 > MAX_NUM or res1 < MIN_NUM:
            self.cpu.c = 1
        else:
            self.cpu.c = 0

    # If the result (after getActualNum convertion) of two positive numbers
    # is negative, or if the result (after convertion) of two negative numbers
    # is positive, sets Overflow Flag to 1.
    def SetOverflow(self, acc, oper, res2):
        if (acc > 0 and oper > 0 and res2 < 0) or
           (acc < 0 and oper < 0 and res2 > 0):
            self.cpu.v = 1
        else:
            self.cpu.v = 0

    # If the result (after getActualNum convertion) of an operation is less
    # than zero, sets Negative Flag to 1.
    def SetNegative(self, res2):
        if res2 < 0:
            self.cpu.n = 1
        else:
            self.cpu.n = 0

    # If the result (after getActualNum convertion) of an operation equals
    # zero, set Zero Flag to 1.
    def SetZero(self, res2):
        if res2 == 0:
            self.cpu.z = 1
        else:
            self.cpu.z = 0

    # If the isBreak argument is set to True, set Break Flag to 1.
    def SetBreak(self, isBreak=False):
        if isBreak:
            self.cpu.b = 1
        else:
            self.cpu.b = 0

    def SetDecimal():
        pass

    def SetInterrupt():
        pass
