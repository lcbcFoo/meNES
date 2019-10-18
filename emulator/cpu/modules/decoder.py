class Decoder():
    def __init__(self, cpu, mem_bus):
        self.cpu = cpu
        self.mem_bus = mem_bus

    def update(self, instr_type):
        # Read 3 bytes starting from address PC (cpu variable).
        opcode, low, high = self.mem_bus.read(self.cpu.pc, 3)

        self.immediate = low
        # Zero page ###########################################################

        if instr_type == 'zeropage':
        # zeropage: ADC oper -- "cont_zp" is the value inside the addres "oper".
            self.cont_zp = self.mem_bus.read(low)
            return

        local_addr_x = low + self.cpu.x
        self.addr_x = local_addr_x % 256

        local_addr_y = low + self.cpu.y
        self.addr_y = local_addr_y % 256

        if instr_type == 'zeropage_x':
        # zeropage,X: ADC oper,X
        # -- "cont_zp_x" is the value inside the addres ("oper" + x).
            self.cont_zp_x = self.mem_bus.read(self.addr_x)
            return

        if instr_type == 'zeropage_y':
        # zeropage,Y: LDX oper,Y
        # -- "cont_zp_y" is the value inside the addres ("oper" + y).
            self.cont_zp_y = self.mem_bus.read(self.addr_y)
            return
        # #####################################################################

        # Absolute ############################################################
        # "full_addr" is the address obtained by concatenating "high"|"low" to
        # get the complete 16-bit address.
        self.full_addr = (high << 8) + low
        self.full_addr_x = (high << 8) + local_addr_x
        self.full_addr_y = (high << 8) + local_addr_y

        if instr_type == 'absolute':
        # absolute: ADC oper -- "content" has the value inside the full address.
            self.content = self.mem_bus.read(self.full_addr)
            return

        if instr_type == 'absolute_x':
        # absolute,X: ADC oper,X
        # -- "content_x" has the value inside the address ("full_addr" + x).
            self.content_x = self.mem_bus.read(self.full_addr_x)
            return

        if instr_type == 'absolute_y':
        # absolute,Y: ADC oper,Y
        # -- "content_y" has the value inside the address ("full_addr" + y).
            self.content_y = self.mem_bus.read(self.full_addr_y)
            return

        # #####################################################################

        # Indirect ############################################################

        if instr_type == 'indirect':
        # indirect: JMP (oper)
        # -- "pointer_addr" is the address where the program will jump to.
            point_low, point_high = self.mem_bus.read(self.full_addr, 2)
            self.pointer_addr = (point_high << 8) + point_low
            return



        if instr_type == 'indirect_x':
        # Indexed indirect
        # (indirect,X): ADC (oper,X)
        # -- "pointer_content_x" is the value used by the instruction.
            point_low_x = self.mem_bus.read(self.addr_x)
            point_high_x = self.mem_bus.read((self.addr_x + 1)%256)
            self.pointer_addr_x = (point_high_x << 8) + point_low_x
            self.pointer_content_x = self.mem_bus.read(self.pointer_addr_x)
            return

        if instr_type == 'indirect_y':
        # Indirect indexed
        # (indirect),Y:  ADC (oper),Y
        # -- "pointer_content_y" is the value used by the instruction.
            point_low_y = self.mem_bus.read(low)
            point_high_y = self.mem_bus.read((low+1)%256)

            self.pointer_addr_y = (point_high_y << 8) + point_low_y + self.cpu.y
            self.pointer_content_y = self.mem_bus.read(self.pointer_addr_y)
            return

        # #####################################################################
