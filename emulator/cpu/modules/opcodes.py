# Dict structure:
# {"opc": Instr(method=method_name(oper), bytes=, cycles=)}

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
    '75': ,                         #ADC
    '35': ,                         #AND
    '16': ,                         #ASL
    'D5': ,                         #CMP
    'D6': ,                         #DEC
    '55': ,                         #EOR
    'F6': ,                         #INC
    'B5': ,                         #LDA
    'B4': ,                         #LDY
    '56': ,                         #LSR
    '15': ,                         #ORA
    '36': ,                         #ROL
    '76': ,                         #ROR
    'F5': ,                         #SBC
    '95': ,                         #STA
    '94': ,                         #STY
}

zeropagey_opodes = {
    'B6': ,                           #LDX
    '96': ,                           #STX
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
