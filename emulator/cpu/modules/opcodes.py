# Dict structure:
# {"opc": Instr(method=class_name.method_name(oper), bytes=, cycles=)}

from collections import namedtuple
from zero_page import ZeroPage
from absolute import Absolute

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
    '65': Instr(method=ZeroPage.zero_page_adc, bytes=2, cycles=3),     #ADC
    '25': Instr(method=ZeroPage.zero_page_and, bytes=2, cycles=3),     #AND
    '06': Instr(method=ZeroPage.zero_page_asl, bytes=2, cycles=5),     #ASL
    '24': Instr(method=ZeroPage.zero_page_bit, bytes=2, cycles=3),     #BIT
    'C5': Instr(method=ZeroPage.zero_page_cmp, bytes=2, cycles=3),     #CMP
    'E4': Instr(method=ZeroPage.zero_page_cpx, bytes=2, cycles=3),     #CPX
    'C4': Instr(method=ZeroPage.zero_page_cpy, bytes=2, cycles=3),     #CPY
    'C6': Instr(method=ZeroPage.zero_page_dec, bytes=2, cycles=5),     #DEC
    '45': Instr(method=ZeroPage.zero_page_eor, bytes=2, cycles=3),     #EOR
    'E6': Instr(method=ZeroPage.zero_page_inc, bytes=2, cycles=5),     #INC
    'A5': Instr(method=ZeroPage.zero_page_lda, bytes=2, cycles=3),     #LDA
    'A6': Instr(method=ZeroPage.zero_page_ldx, bytes=2, cycles=3),     #LDX
    'A4': Instr(method=ZeroPage.zero_page_ldy, bytes=2, cycles=3),     #LDY
    '46': Instr(method=ZeroPage.zero_page_lsr, bytes=2, cycles=5),     #LSR
    '05': Instr(method=ZeroPage.zero_page_ora, bytes=2, cycles=3),     #ORA
    '26': Instr(method=ZeroPage.zero_page_rol, bytes=2, cycles=5),     #ROL
    '66': Instr(method=ZeroPage.zero_page_ror, bytes=2, cycles=5),     #ROR
    'E5': Instr(method=ZeroPage.zero_page_sbc, bytes=2, cycles=3),     #SBC
    '85': Instr(method=ZeroPage.zero_page_sta, bytes=2, cycles=3),     #STA
    '86': Instr(method=ZeroPage.zero_page_stx, bytes=2, cycles=3),     #STX
    '84': Instr(method=ZeroPage.zero_page_sty, bytes=2, cycles=3),     #STY
}

zeropagex_opcodes = {
    'D6': Instr(method=ZeroPage.zpx_dec, bytes=2, cycles=6),        #DEC
    '55': Instr(method=ZeroPage.zpx_eor, bytes=2, cycles=4),        #EOR
    '75': Instr(method=ZeroPage.zpx_adc, bytes=2, cycles=4),        #ADC
    '35': Instr(method=ZeroPage.zpx_and, bytes=2, cycles=4),        #AND
    '16': Instr(method=ZeroPage.zpx_asl, bytes=2, cycles=6),        #ASL
    'D5': Instr(method=ZeroPage.zpx_cmp, bytes=2, cycles=4),        #CMP
    'F6': Instr(method=ZeroPage.zpx_inc, bytes=2, cycles=6),        #INC
    'B5': Instr(method=ZeroPage.zpx_lda, bytes=2, cycles=4),        #LDA
    'B4': Instr(method=ZeroPage.zpx_ldy, bytes=2, cycles=4),        #LDY
    '56': Instr(method=ZeroPage.zpx_lsr, bytes=2, cycles=6),        #LSR
    '15': Instr(method=ZeroPage.zpx_ora, bytes=2, cycles=4),        #ORA
    '36': Instr(method=ZeroPage.zpx_rol, bytes=2, cycles=6),        #ROL
    '76': Instr(method=ZeroPage.zpx_ror, bytes=2, cycles=6),        #ROR
    'F5': Instr(method=ZeroPage.zpx_sbc, bytes=2, cycles=4),        #SBC
    '95': Instr(method=ZeroPage.zpx_sta, bytes=2, cycles=4),        #STA
    '94': Instr(method=ZeroPage.zpx_sty, bytes=2, cycles=4),        #STY
}

zeropagey_opodes = {
    'B6': Instr(method=ZeroPage.zpy_ldx, bytes=2, cycles=4),        #LDX
    '96': Instr(method=ZeroPage.zpy_stx, bytes=2, cycles=4),        #STX
}

absolute_opcodes = {
    '6D': Instr(method=Absolute.abs_adc, bytes=3, cycles=4),                         #ADC
    '2D': Instr(method=Absolute.abs_and, bytes=, cycles=),                         #AND
    '0E': Instr(method=Absolute.abs_asl, bytes=, cycles=),                         #ASL
    '2C': Instr(method=Absolute.abs_bit, bytes=, cycles=),                         #BIT
    'CD': Instr(method=Absolute.abs_cmp, bytes=, cycles=),                         #CMP
    'EC': Instr(method=Absolute.abs_cpx, bytes=, cycles=),                         #CPX
    'CC': Instr(method=Absolute.abs_cpy, bytes=, cycles=),                         #CPY
    'CE': Instr(method=Absolute.abs_dec, bytes=, cycles=),                         #DEC
    '4D': Instr(method=Absolute.abs_eor, bytes=, cycles=),                         #EOR
    'EE': Instr(method=Absolute.abs_inc, bytes=, cycles=),                         #INC
    '4C': Instr(method=Absolute.abs_jmp, bytes=, cycles=),                         #JMP
    '20': Instr(method=Absolute.abs_jsr, bytes=, cycles=),                         #JSR
    'AD': Instr(method=Absolute.abs_lda, bytes=, cycles=),                         #LDA
    'AE': Instr(method=Absolute.abs_ldx, bytes=, cycles=),                         #LDX
    'AC': Instr(method=Absolute.abs_ldy, bytes=, cycles=),                         #LDY
    '4E': Instr(method=Absolute.abs_lsr, bytes=, cycles=),                         #LSR
    '0D': Instr(method=Absolute.abs_ora, bytes=, cycles=),                         #ORA
    '2E': Instr(method=Absolute.abs_rol, bytes=, cycles=),                         #ROL
    '6E': Instr(method=Absolute.abs_ror, bytes=, cycles=),                         #ROR
    'ED': Instr(method=Absolute.abs_sbc, bytes=, cycles=),                         #SBC
    '8D': Instr(method=Absolute.abs_sta, bytes=, cycles=),                         #STA
    '8E': Instr(method=Absolute.abs_stx, bytes=, cycles=),                         #STX
    '8C': Instr(method=Absolute.abs_sty, bytes=, cycles=),                         #STY
}

absolutex_opcodes = {
    '7D': Instr(method=Absolute.absX_adc, bytes=, cycles=),                         #ADC
    '3D': Instr(method=Absolute.absX_and, bytes=, cycles=),                         #AND
    '1E': Instr(method=Absolute.absX_asl, bytes=, cycles=),                         #ASL
    'DD': Instr(method=Absolute.absX_cmp, bytes=, cycles=),                         #CMP
    'DE': Instr(method=Absolute.absX_dec, bytes=, cycles=),                         #DEC
    '5D': Instr(method=Absolute.absX_eor, bytes=, cycles=),                         #EOR
    'FE': Instr(method=Absolute.absX_inc, bytes=, cycles=),                         #INC
    'BD': Instr(method=Absolute.absX_lda, bytes=, cycles=),                         #LDA
    'BC': Instr(method=Absolute.absX_ldy, bytes=, cycles=),                         #LDY
    '5E': Instr(method=Absolute.absX_lsr, bytes=, cycles=),                         #LSR
    '1D': Instr(method=Absolute.absX_ora, bytes=, cycles=),                         #ORA
    '3E': Instr(method=Absolute.absX_rol, bytes=, cycles=),                         #ROL
    '7E': Instr(method=Absolute.absX_ror, bytes=, cycles=),                         #ROR
    'FD': Instr(method=Absolute.absX_sbc, bytes=, cycles=),                         #SBC
    '9D': Instr(method=Absolute.absX_sta, bytes=, cycles=),                         #STA
}

absolutey_opcodes = {
    '79': Instr(method=Absolute.absY_adc, bytes=, cycles=),                         #ADC
    '39': Instr(method=Absolute.absY_and, bytes=, cycles=),                         #AND
    'D9': Instr(method=Absolute.absY_cmp, bytes=, cycles=),                         #CMP
    '59': Instr(method=Absolute.absY_eor, bytes=, cycles=),                         #EOR
    'B9': Instr(method=Absolute.absY_lda, bytes=, cycles=),                         #LDA
    'BE': Instr(method=Absolute.absY_ldx, bytes=, cycles=),                         #LDX
    '19': Instr(method=Absolute.absY_ora, bytes=, cycles=),                         #ORA
    'F9': Instr(method=Absolute.absY_sbc, bytes=, cycles=),                         #SBC
    '99': Instr(method=Absolute.absY_sta, bytes=, cycles=),                         #STA
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
