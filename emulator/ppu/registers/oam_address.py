class OAMADDR:

    def __init__(self):
        self.reg = 0

    # The register value remains unchanged after reset
    def reset():
        pass

    def write(self, value):
        self.reg = value
