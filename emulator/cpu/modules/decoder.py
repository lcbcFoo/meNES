
class Decoder():

    # Read 3 bytes starting from address PC (cpu variable).
    opcode, low, high = MemoryBus.read(self.cpu.pc, 3)


    # Zero page ###############################################################

    # zeropage: ADC oper -- "cont_zp" is the value inside the addres "oper".
    cont_zp = MemoryBus.read(low)

    # zeropage,X: ADC oper,X
    # -- "cont_zp_x" is the value inside the addres ("oper" + x).
    cont_zp_x = MemoryBus.read(low + self.cpu.x)

    # zeropage,Y: LDX oper,Y
    # -- "cont_zp_y" is the value inside the addres ("oper" + y).
    cont_zp_y = MemoryBus.read(low + self.cpu.y)
    # #########################################################################

    # Absolute ################################################################
    # "full_addr" is the address obtained by concatenating "high"|"low" to get
    # the complete 16-bit address.
    full_addr = (high * 2**8) + low

    # absolute: ADC oper -- "content" has the value inside the full address.
    content = MemoryBus.read(full_addr)

    # absolute,X: ADC oper,X
    # -- "content_x" has the value inside the address ("full_addr" + x).
    content_x = MemoryBus.read(full_addr + self.cpu.x)

    # absolute,Y: ADC oper,Y
    # -- "content_y" has the value inside the address ("full_addr" + y).
    content_y = MemoryBus.read(full_addr + self.cpu.y)

    # #########################################################################

    # Indirect ################################################################

    # indirect: JMP (oper)
    # -- "pointer_addr" is the address where the program will jump to.
    point_low, point_high = MemoryBus.read(full_addr, 2)
    pointer_addr = (point_high * 2**8) + point_low

    # Indexed indirect
    # (indirect,X): ADC (oper,X)
    # -- "pointer_content_x" is the value used by the instruction.
    ind_addr_x = low + self.cpu.x
    point_low_x, point_high_x = MemoryBus.read(ind_addr_x, 2)
    pointer_addr_x = (point_high_x * 2**8) + point_low_x
    pointer_content_x = MemoryBus.read(pointer_addr_x)

    # Indirect indexed
    # (indirect),Y  ADC (oper),Y
    # -- "pointer_content_y" is the value used by the instruction.
    point_low_y, point_high_y = MemoryBus.read(low, 2)
    pointer_addr_y = (point_high_y * 2**8) + point_low_y + self.cpu.y
    pointer_content_y = MemoryBus.read(pointer_addr_y)

    # #########################################################################
