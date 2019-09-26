class Decoder():
    def __init__(self, cpu, mem_bus):
        self.cpu = cpu
        self.mem_bus = mem_bus

    def update(self):
        # Read 3 bytes starting from address PC (cpu variable).
        self.opcode, low, high = self.mem_bus.read(self.cpu.pc, 3)

        self.immediate = low
        # Zero page ###########################################################

        # zeropage: ADC oper -- "cont_zp" is the value inside the addres "oper".
        self.cont_zp = self.mem_bus.read(low)

        reg_x = self.cpu.x
        if reg_x >= 0x80:
            new_addr_x = low - (~(reg_x - 1) % 256)
            if new_addr_x >= 0:
                self.addr_x = new_addr_x
            else:
                self.addr_x = low + reg_x
        else:
            self.addr_x = low + reg_x

        reg_y = self.cpu.y
        if reg_y >= 0x80:
            new_addr_y = low - (~(reg_y - 1) % 256)
            if new_addr_y >= 0:
                self.addr_y = new_addr_y
            else:
                self.addr_y = low + reg_y
        else:
            self.addr_y = low + reg_y

        # zeropage,X: ADC oper,X
        # -- "cont_zp_x" is the value inside the addres ("oper" + x).
        self.cont_zp_x = self.mem_bus.read(self.addr_x)

        # zeropage,Y: LDX oper,Y
        # -- "cont_zp_y" is the value inside the addres ("oper" + y).
        self.cont_zp_y = self.mem_bus.read(self.addr_y)
        # #####################################################################

        # Absolute ############################################################
        # "full_addr" is the address obtained by concatenating "high"|"low" to
        # get the complete 16-bit address.
        self.full_addr = (high << 8) + low
        self.full_addr_x = (high << 8) + self.addr_x
        self.full_addr_y = (high << 8) + self.addr_y

        # absolute: ADC oper -- "content" has the value inside the full address.
        self.content = self.mem_bus.read(self.full_addr)

        # absolute,X: ADC oper,X
        # -- "content_x" has the value inside the address ("full_addr" + x).
        self.content_x = self.mem_bus.read(self.full_addr_x)

        # absolute,Y: ADC oper,Y
        # -- "content_y" has the value inside the address ("full_addr" + y).
        self.content_y = self.mem_bus.read(self.full_addr_y)

        # #####################################################################

        # Indirect ############################################################

        # indirect: JMP (oper)
        # -- "pointer_addr" is the address where the program will jump to.
        point_low, point_high = self.mem_bus.read(self.full_addr, 2)
        self.pointer_addr = (point_high << 8) + point_low

        # Indexed indirect
        # (indirect,X): ADC (oper,X)
        # -- "pointer_content_x" is the value used by the instruction.
        point_low_x, point_high_x = self.mem_bus.read(self.addr_x, 2)
        pointer_addr_x = (point_high_x << 8) + point_low_x
        self.pointer_content_x = self.mem_bus.read(pointer_addr_x)

        # Indirect indexed
        # (indirect),Y:  ADC (oper),Y
        # -- "pointer_content_y" is the value used by the instruction.
        point_low_y, point_high_y = self.mem_bus.read(low, 2)

        if reg_y >= 0x80:
            np_low_y = point_low_y - (~(reg_y - 1) % 256)
        else:
            np_low_y = point_low_y + reg_y

        pointer_addr_y = (point_high_y << 8) + np_low_y
        self.pointer_content_y = self.mem_bus.read(pointer_addr_y)

        # #####################################################################
