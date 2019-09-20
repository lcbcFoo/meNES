

# NOTATION
# res: represents the result of an operation in decimal values. Could be any
#       number.
# res_8b: represents the same result as a two's complement of an 8-bit number.
#
# Before using any methods with parameter called "res_8b", first call the method
# getActualNum() to convert res into an res_8b format number.
class FlagHandler():
    MAX_NUM = 255
    NEGATIVE = 128
    def __init__(self, cpu):
        self.cpu = cpu

    # Transforms a number into the a two's complement 8-bit number that fits
    # inside the register.
    def getActualNum(self, res):
        return res % (self.MAX_NUM + 1)


    # If the result of an operation is bigger than MAX_NUM or smaller than
    # MIN_NUM, sets the Carry Flag to 1.
    def setCarry(self, res):
        if res > self.MAX_NUM:
            self.cpu.c = 1
        else:
            self.cpu.c = 0

    # The carry flag is set if the result is greater than or equal to 0.
    # The carry flag is reset when the result is less than 0, indicating a
    # borrow.
    def setCarrySbc(self, res):
        if res < self.NEGATIVE:   # if res is a positive number
            self.cpu.c = 1
        else:
            self.cpu.c = 0

    # If the result (after getActualNum convertion) of two positive numbers
    # is negative, or if the result (after convertion) of two negative numbers
    # is positive, sets Overflow Flag to 1.
    def setOverflow(self, acc, oper, res_8b):
        if ((acc < self.NEGATIVE and oper < self.NEGATIVE and res_8b >= self.NEGATIVE)
         or (acc >= self.NEGATIVE and oper >= self.NEGATIVE and res_8b < self.NEGATIVE)):
            self.cpu.v = 1
        else:
            self.cpu.v = 0

    # The overflow flag is set when the result exceeds +127 or -127, otherwise
    # it is reset.
    # def setOverflowSbc(self, res):
    #     if res < 0 or res > self.MAX_NUM:
    #         self.cpu.v = 1
    #     else:
    #         self.cpu.v = 0

    # If the result (after getActualNum convertion) of an operation is less
    # than zero, sets Negative Flag to 1.
    def setNegative(self, res_8b):
        if res_8b >= self.NEGATIVE:
            self.cpu.n = 1
        else:
            self.cpu.n = 0

    # If the result (after getActualNum convertion) of an operation equals
    # zero, set Zero Flag to 1.
    def setZero(self, res_8b):
        if res_8b == 0:
            self.cpu.z = 1
        else:
            self.cpu.z = 0

    # If the isBreak argument is set to True, set Break Flag to 1.
    def setBreak(self, isBreak=False):
        if isBreak:
            self.cpu.b = 1
        else:
            self.cpu.b = 0

    def setDecimal(self, isDecimal=False):
        if isDecimal:
            self.cpu.d = 1
        else:
            self.cpu.d = 0

    def setInterrupt(self, isInterrupt=False):
        if isInterrupt:
            self.cpu.i = 1
        else:
            self.cpu.i = 0
