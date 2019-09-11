# Dict structure:
# {"opc": Instr(method=class_name.method_name(oper), bytes=, cycles=)}

from collections import namedtuple

Instr = namedtuple('Instr', 'method bytes cycles')


immediate_opcodes = {
    '69': ,                         #ADC
    '29': ,                         #AND
    'C9': ,                         #CMP
    'E0': ,                         #CPX
    'C0': ,                         #CPY
    '49': ,                         #EOR
    'A9': ,                         #LDA
    'A2': ,                         #LDX
    'A0': ,                         #LDY
    '09': ,                         #ORA
    'E9':                           #SBC
}

zeropage_opcodes = {
    '65': Instr(method=zero_page_adc(oper), bytes=2, cycles=3),     #ADC
    '25': Instr(method=zero_page_and(oper), bytes=2, cycles=3),     #AND
    '06': Instr(method=zero_page_asl(oper), bytes=2, cycles=5),     #ASL
    '24': Instr(method=zero_page_bit(oper), bytes=2, cycles=3),     #BIT
    'C5': Instr(method=zero_page_cmp(oper), bytes=2, cycles=3),     #CMP
    'E4': Instr(method=zero_page_cpx(oper), bytes=2, cycles=3),     #CPX
    'C4': Instr(method=zero_page_cpy(oper), bytes=2, cycles=3),     #CPY
    'C6': Instr(method=zero_page_dec(oper), bytes=2, cycles=5),     #DEC
    '45': Instr(method=zero_page_eor(oper), bytes=2, cycles=3),     #EOR
    'E6': Instr(method=zero_page_inc(oper), bytes=2, cycles=5),     #INC
    'A5': Instr(method=zero_page_lda(oper), bytes=2, cycles=3),     #LDA
    'A6': Instr(method=zero_page_ldx(oper), bytes=2, cycles=3),     #LDX
    'A4': Instr(method=zero_page_ldy(oper), bytes=2, cycles=3),     #LDY
    '46': Instr(method=zero_page_lsr(oper), bytes=2, cycles=5),     #LSR
    '05': Instr(method=zero_page_ora(oper), bytes=2, cycles=3),     #ORA
    '26': Instr(method=zero_page_rol(oper), bytes=2, cycles=5),     #ROL
    '66': Instr(method=zero_page_ror(oper), bytes=2, cycles=5),     #ROR
    'E5': Instr(method=zero_page_sbc(oper), bytes=2, cycles=3),     #SBC
    '85': Instr(method=zero_page_sta(oper), bytes=2, cycles=3),     #STA
    '86': Instr(method=zero_page_stx(oper), bytes=2, cycles=3),     #STX
    '84': Instr(method=zero_page_sty(oper), bytes=2, cycles=3),     #STY
}

zeropagex_opcodes = {
    '75': Instr(method=zpx_adc(oper, X), bytes=2, cycles=4),                         #ADC
    '35': Instr(method=zpx_and(oper, X), bytes=2, cycles=4),                         #AND
    '16': Instr(method=zpx_asl(oper, X), bytes=2, cycles=6),                         #ASL
    'D5': Instr(method=zpx_cmp(oper, X), bytes=2, cycles=4),                         #CMP
    'D6': Instr(method=zpx_dec(oper, X), bytes=2, cycles=6),                         #DEC
    '55': Instr(method=zpx_eor(oper, X), bytes=2, cycles=4),                         #EOR
    'F6': Instr(method=zpx_inc(oper, X), bytes=2, cycles=6),                         #INC
    'B5': Instr(method=zpx_lda(oper, X), bytes=2, cycles=4),                         #LDA
    'B4': Instr(method=zpx_ldy(oper, X), bytes=2, cycles=4),                         #LDY
    '56': Instr(method=zpx_lsr(oper, X), bytes=2, cycles=6),                         #LSR
    '15': Instr(method=zpx_ora(oper, X), bytes=2, cycles=4),                         #ORA
    '36': Instr(method=zpx_rol(oper, X), bytes=2, cycles=6),                         #ROL
    '76': Instr(method=zpx_ror(oper, X), bytes=2, cycles=6),                         #ROR
    'F5': Instr(method=zpx_sbc(oper, X), bytes=2, cycles=4),                         #SBC
    '95': Instr(method=zpx_sta(oper, X), bytes=2, cycles=4),                         #STA
    '94': Instr(method=zpx_sty(oper, X), bytes=2, cycles=4),                         #STY
}

zeropagey_opodes = {
    'B6': Instr(method=zpy_ldx(oper, Y), bytes=2, cycles=4),                           #LDX
    '96': Instr(method=zpy_stx(oper, Y), bytes=2, cycles=4),                           #STX
}

absolute_opcodes = {
    '6D': ,                         #ADC
    '2D': ,                         #AND
    '0E': ,                         #ASL
    '2C': ,                         #BIT
    'CD': ,                         #CMP
    'EC': ,                         #CPX
    'CC': ,                         #CPY
    'CE': ,                         #DEC
    '4D': ,                         #EOR
    'EE': ,                         #INC
    '4C': ,                         #JMP
    '20': ,                         #JSR
    'AD': ,                         #LDA
    'AE': ,                         #LDX
    'AC': ,                         #LDY
    '4E': ,                         #LSR
    '0D': ,                         #ORA
    '2E': ,                         #ROL
    '6E': ,                         #ROR
    'ED': ,                         #SBC
    '8D': ,                         #STA
    '8E': ,                         #STX
    '8C': ,                         #STY
}

absolutex_opcodes = {
    '7D': ,                         #ADC
    '3D': ,                         #AND
    '1E': ,                         #ASL
    'DD': ,                         #CMP
    'DE': ,                         #DEC
    '5D': ,                         #EOR
    'FE': ,                         #INC
    'BD': ,                         #LDA
    'BC': ,                         #LDY
    '5E': ,                         #LSR
    '1D': ,                         #ORA
    '3E': ,                         #ROL
    '7E': ,                         #ROR
    'FD': ,                         #SBC
    '9D': ,                         #STA
}

absolutey_opcodes = {
    '79': ,                         #ADC
    '39': ,                         #AND
    'D9': ,                         #CMP
    '59': ,                         #EOR
    'B9': ,                         #LDA
    'BE': ,                         #LDX
    '19': ,                         #ORA
    'F9': ,                         #SBC
    '99': ,                         #STA
}

indirect_opcodes = {
    '6C': ,                         #JMP
}

indirectx_opcodes = {
    '61': ,                         #ADC
    '21': ,                         #AND
    'C1': ,                         #CMP
    '41': ,                         #EOR
    'A1': ,                         #LDA
    '01': ,                         #ORA
    'E1': ,                         #SBC
    '81': ,                         #STA

}

indirecty_opcodes = {
    '71': ,                         #ADC
    '31': ,                         #AND
    'D1': ,                         #CMP
    '51': ,                         #EOR
    'B1': ,                         #LDA
    '11': ,                         #ORA
    'F1': ,                         #SBC
    '91': ,                         #STA
}

implied_opcodes = {
    '00': ,                         #BRK
    'EA': ,                         #NOP
    '40': ,                         #RTI
    '60': ,                         #RTS

    '18': ,                         #CLC
    '38': ,                         #SEC
    '58': ,                         #CLI
    '78': ,                         #SEI
    'B8': ,                         #CLV
    'D8': ,                         #CLD
    'F8': ,                         #SED

    '9A': ,                         #TXS
    'BA': ,                         #TSX
    '48': ,                         #PHA
    '68': ,                         #PLA
    '08': ,                         #PHP
    '28': ,                         #PLP

    'AA': ,                         #TAX
    '8A': ,                         #TXA
    'CA': ,                         #DEX
    'E8': ,                         #INX
    'A8': ,                         #TAY
    '98': ,                         #TYA
    '88': ,                         #DEY
    'C8': ,                         #INY
}

relative_opcodes = {
    '10': ,                         #BPL
    '30': ,                         #BMI
    '50': ,                         #BVC
    '70': ,                         #BVS
    '90': ,                         #BCC
    'B0': ,                         #BCS
    'D0': ,                         #BNE
    'F0': ,                         #BEQ
}

accumulator_opcodes = {
    '0A': ,                         #ASL
    '4A': ,                         #LSR
    '2A': ,                         #ROL
    '6A': ,                         #ROR
}
