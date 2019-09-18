MAX_NUM = 255
NEGATIVE = 128

# NOTATION
# res: represents the result of an operation in decimal values. Could be any
#       number.
# res_8b: represents the same result as a two's complement of an 8-bit number.
#
# Before using any methods with parameter called "res_8b", first call the method
# getActualNum() to convert res into an res_8b format number.

class FlagHandler():

    def __init__(self, cpu):
        self.cpu = cpu

    # Transforms a number into the a two's complement 8-bit number that fits
    # inside the register.
    def getActualNum(self, res):
        return res % (MAX_NUM + 1)


    # If the result of an operation is bigger than MAX_NUM or smaller than
    # MIN_NUM, sets the Carry Flag to 1.
    def SetCarry(self, res):
        if res > MAX_NUM:
            self.cpu.c = 1
        else:
            self.cpu.c = 0

    # If the result (after getActualNum convertion) of two positive numbers
    # is negative, or if the result (after convertion) of two negative numbers
    # is positive, sets Overflow Flag to 1.
    def SetOverflow(self, acc, oper, res_8b):
        if (acc < NEGATIVE and oper < NEGATIVE and res_8b >= NEGATIVE) or
           (acc >= NEGATIVE and oper >= NEGATIVE and res_8b < NEGATIVE):
            self.cpu.v = 1
        else:
            self.cpu.v = 0

    # If the result (after getActualNum convertion) of an operation is less
    # than zero, sets Negative Flag to 1.
    def SetNegative(self, res_8b):
        if res_8b >= NEGATIVE:
            self.cpu.n = 1
        else:
            self.cpu.n = 0

    # If the result (after getActualNum convertion) of an operation equals
    # zero, set Zero Flag to 1.
    def SetZero(self, res_8b):
        if res_8b == 0:
            self.cpu.z = 1
        else:
            self.cpu.z = 0

    # If the isBreak argument is set to True, set Break Flag to 1.
    def SetBreak(self, isBreak=False):
        if isBreak:
            self.cpu.b = 1
        else:
            self.cpu.b = 0

    def SetDecimal(self, isDecimal=False):
        if isDecimal:
            self.cpu.d = 1
        else:
            self.cpu.d = 0

    def SetInterrupt(self, isInterrupt=False):
        if isInterrupt:
            self.cpu.i = 1
        else:
            self.cpu.i = 0
