class Decoder():
    def __init__(self, cpu, mem_bus):
        # Read 3 bytes starting from address PC (cpu variable).
        self.opcode, low, high = mem_bus.read(cpu.pc, 3)

        self.immediate = low
        # Zero page ###########################################################

        # zeropage: ADC oper -- "cont_zp" is the value inside the addres "oper".
        self.cont_zp = mem_bus.read(low)

        # zeropage,X: ADC oper,X
        # -- "cont_zp_x" is the value inside the addres ("oper" + x).
        self.cont_zp_x = mem_bus.read(low + cpu.x)

        # zeropage,Y: LDX oper,Y
        # -- "cont_zp_y" is the value inside the addres ("oper" + y).
        self.cont_zp_y = mem_bus.read(low + cpu.y)
        # #####################################################################

        # Absolute ############################################################
        # "full_addr" is the address obtained by concatenating "high"|"low" to
        # get the complete 16-bit address.
        full_addr = (high * 2**8) + low

        # absolute: ADC oper -- "content" has the value inside the full address.
        self.content = mem_bus.read(full_addr)

        # absolute,X: ADC oper,X
        # -- "content_x" has the value inside the address ("full_addr" + x).
        self.content_x = mem_bus.read(full_addr + cpu.x)

        # absolute,Y: ADC oper,Y
        # -- "content_y" has the value inside the address ("full_addr" + y).
        self.content_y = mem_bus.read(full_addr + cpu.y)

        # #####################################################################

        # Indirect ############################################################

        # indirect: JMP (oper)
        # -- "pointer_addr" is the address where the program will jump to.
        point_low, point_high = mem_bus.read(full_addr, 2)
        self.pointer_addr = (point_high * 2**8) + point_low

        # Indexed indirect
        # (indirect,X): ADC (oper,X)
        # -- "pointer_content_x" is the value used by the instruction.
        ind_addr_x = low + cpu.x
        point_low_x, point_high_x = mem_bus.read(ind_addr_x, 2)
        pointer_addr_x = (point_high_x * 2**8) + point_low_x
        self.pointer_content_x = mem_bus.read(pointer_addr_x)

        # Indirect indexed
        # (indirect),Y  ADC (oper),Y
        # -- "pointer_content_y" is the value used by the instruction.
        point_low_y, point_high_y = mem_bus.read(low, 2)
        pointer_addr_y = (point_high_y * 2**8) + point_low_y + cpu.y
        self.pointer_content_y = mem_bus.read(pointer_addr_y)

        # #####################################################################
