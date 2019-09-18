# Dict structure:
# {"opc": Instr(method=class_name.method_name(oper), bytes=, cycles=)}

from collections import namedtuple
from zero_page import ZeroPage
from absolute import Absolute
from immediate import Immediate
from implied import Implied

Instr = namedtuple('Instr', 'method bytes cycles')


immediate_opcodes = {
    '69': Instr(method=Imediate.imd_adc, bytes=2, cycles=2),           #ADC
    '29': Instr(method=Imediate.imd_and, bytes=2, cycles=2),           #AND
    'C9': Instr(method=Imediate.imd_cmp, bytes=2, cycles=2),           #CMP
    'E0': Instr(method=Imediate.imd_cpx, bytes=2, cycles=2),           #CPX
    'C0': Instr(method=Imediate.imd_cpy, bytes=2, cycles=2),           #CPY
    '49': Instr(method=Imediate.imd_eor, bytes=2, cycles=2),           #EOR
    'A9': Instr(method=Imediate.imd_lda, bytes=2, cycles=2),           #LDA
    'A2': Instr(method=Imediate.imd_ldx, bytes=2, cycles=2),           #LDX
    'A0': Instr(method=Imediate.imd_ldy, bytes=2, cycles=2),           #LDY
    '09': Instr(method=Imediate.imd_ora, bytes=2, cycles=2),           #ORA
    'E9': Instr(method=Imediate.imd_sbc, bytes=2, cycles=2)            #SBC
}

zeropage_opcodes = {
    '65': Instr(method=ZeroPage.zp_adc, bytes=2, cycles=3),     #ADC
    '25': Instr(method=ZeroPage.zp_and, bytes=2, cycles=3),     #AND
    '06': Instr(method=ZeroPage.zp_asl, bytes=2, cycles=5),     #ASL
    '24': Instr(method=ZeroPage.zp_bit, bytes=2, cycles=3),     #BIT
    'C5': Instr(method=ZeroPage.zp_cmp, bytes=2, cycles=3),     #CMP
    'E4': Instr(method=ZeroPage.zp_cpx, bytes=2, cycles=3),     #CPX
    'C4': Instr(method=ZeroPage.zp_cpy, bytes=2, cycles=3),     #CPY
    'C6': Instr(method=ZeroPage.zp_dec, bytes=2, cycles=5),     #DEC
    '45': Instr(method=ZeroPage.zp_eor, bytes=2, cycles=3),     #EOR
    'E6': Instr(method=ZeroPage.zp_inc, bytes=2, cycles=5),     #INC
    'A5': Instr(method=ZeroPage.zp_lda, bytes=2, cycles=3),     #LDA
    'A6': Instr(method=ZeroPage.zp_ldx, bytes=2, cycles=3),     #LDX
    'A4': Instr(method=ZeroPage.zp_ldy, bytes=2, cycles=3),     #LDY
    '46': Instr(method=ZeroPage.zp_lsr, bytes=2, cycles=5),     #LSR
    '05': Instr(method=ZeroPage.zp_ora, bytes=2, cycles=3),     #ORA
    '26': Instr(method=ZeroPage.zp_rol, bytes=2, cycles=5),     #ROL
    '66': Instr(method=ZeroPage.zp_ror, bytes=2, cycles=5),     #ROR
    'E5': Instr(method=ZeroPage.zp_sbc, bytes=2, cycles=3),     #SBC
    '85': Instr(method=ZeroPage.zp_sta, bytes=2, cycles=3),     #STA
    '86': Instr(method=ZeroPage.zp_stx, bytes=2, cycles=3),     #STX
    '84': Instr(method=ZeroPage.zp_sty, bytes=2, cycles=3),     #STY
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
    '2D': Instr(method=Absolute.abs_and, bytes=3, cycles=4),                         #AND
    '0E': Instr(method=Absolute.abs_asl, bytes=3, cycles=6),                         #ASL
    '2C': Instr(method=Absolute.abs_bit, bytes=3, cycles=4),                         #BIT
    'CD': Instr(method=Absolute.abs_cmp, bytes=3, cycles=4),                         #CMP
    'EC': Instr(method=Absolute.abs_cpx, bytes=3, cycles=4),                         #CPX
    'CC': Instr(method=Absolute.abs_cpy, bytes=3, cycles=4),                         #CPY
    'CE': Instr(method=Absolute.abs_dec, bytes=3, cycles=6),                         #DEC
    '4D': Instr(method=Absolute.abs_eor, bytes=3, cycles=4),                         #EOR
    'EE': Instr(method=Absolute.abs_inc, bytes=3, cycles=6),                         #INC
    '4C': Instr(method=Absolute.abs_jmp, bytes=3, cycles=3),                         #JMP
    '20': Instr(method=Absolute.abs_jsr, bytes=3, cycles=6),                         #JSR
    'AD': Instr(method=Absolute.abs_lda, bytes=3, cycles=4),                         #LDA
    'AE': Instr(method=Absolute.abs_ldx, bytes=3, cycles=4),                         #LDX
    'AC': Instr(method=Absolute.abs_ldy, bytes=3, cycles=4),                         #LDY
    '4E': Instr(method=Absolute.abs_lsr, bytes=3, cycles=6),                         #LSR
    '0D': Instr(method=Absolute.abs_ora, bytes=3, cycles=4),                         #ORA
    '2E': Instr(method=Absolute.abs_rol, bytes=3, cycles=6),                         #ROL
    '6E': Instr(method=Absolute.abs_ror, bytes=3, cycles=6),                         #ROR
    'ED': Instr(method=Absolute.abs_sbc, bytes=3, cycles=4),                         #SBC
    '8D': Instr(method=Absolute.abs_sta, bytes=3, cycles=4),                         #STA
    '8E': Instr(method=Absolute.abs_stx, bytes=3, cycles=4),                         #STX
    '8C': Instr(method=Absolute.abs_sty, bytes=3, cycles=4),                         #STY
}

absolutex_opcodes = {
    '7D': Instr(method=Absolute.absX_adc, bytes=3, cycles=4),                         #ADC
    '3D': Instr(method=Absolute.absX_and, bytes=3, cycles=4),                         #AND
    '1E': Instr(method=Absolute.absX_asl, bytes=3, cycles=7),                         #ASL
    'DD': Instr(method=Absolute.absX_cmp, bytes=3, cycles=4),                         #CMP
    'DE': Instr(method=Absolute.absX_dec, bytes=3, cycles=7),                         #DEC
    '5D': Instr(method=Absolute.absX_eor, bytes=3, cycles=4),                         #EOR
    'FE': Instr(method=Absolute.absX_inc, bytes=3, cycles=7),                         #INC
    'BD': Instr(method=Absolute.absX_lda, bytes=3, cycles=4),                         #LDA
    'BC': Instr(method=Absolute.absX_ldy, bytes=3, cycles=4),                         #LDY
    '5E': Instr(method=Absolute.absX_lsr, bytes=3, cycles=7),                         #LSR
    '1D': Instr(method=Absolute.absX_ora, bytes=3, cycles=4),                         #ORA
    '3E': Instr(method=Absolute.absX_rol, bytes=3, cycles=7),                         #ROL
    '7E': Instr(method=Absolute.absX_ror, bytes=3, cycles=7),                         #ROR
    'FD': Instr(method=Absolute.absX_sbc, bytes=3, cycles=4),                         #SBC
    '9D': Instr(method=Absolute.absX_sta, bytes=3, cycles=5),                         #STA
}

absolutey_opcodes = {
    '79': Instr(method=Absolute.absY_adc, bytes=3, cycles=4),                         #ADC
    '39': Instr(method=Absolute.absY_and, bytes=3, cycles=4),                         #AND
    'D9': Instr(method=Absolute.absY_cmp, bytes=3, cycles=4),                         #CMP
    '59': Instr(method=Absolute.absY_eor, bytes=3, cycles=4),                         #EOR
    'B9': Instr(method=Absolute.absY_lda, bytes=3, cycles=4),                         #LDA
    'BE': Instr(method=Absolute.absY_ldx, bytes=3, cycles=4),                         #LDX
    '19': Instr(method=Absolute.absY_ora, bytes=3, cycles=4),                         #ORA
    'F9': Instr(method=Absolute.absY_sbc, bytes=3, cycles=4),                         #SBC
    '99': Instr(method=Absolute.absY_sta, bytes=3, cycles=5),                         #STA
}

# indirect_opcodes = {
#     '6C': ,                         #JMP
# }

# indirectx_opcodes = {
#     '61': ,                         #ADC
#     '21': ,                         #AND
#     'C1': ,                         #CMP
#     '41': ,                         #EOR
#     'A1': ,                         #LDA
#     '01': ,                         #ORA
#     'E1': ,                         #SBC
#     '81': ,                         #STA

# }

# indirecty_opcodes = {
#     '71': ,                         #ADC
#     '31': ,                         #AND
#     'D1': ,                         #CMP
#     '51': ,                         #EOR
#     'B1': ,                         #LDA
#     '11': ,                         #ORA
#     'F1': ,                         #SBC
#     '91': ,                         #STA
# }

implied_opcodes = {
    '00': Instr(method=Implide.imp_brk, bytes=1, cycles=7),         #BRK
    'EA': Instr(method=Implide.imp_nop, bytes=1, cycles=2),         #NOP
    '40': Instr(method=Implide.imp_rti, bytes=1, cycles=6),         #RTI
    '60': Instr(method=Implide.imp_rts, bytes=1, cycles=6),         #RTS

    '18': Instr(method=Implide.imp_clc, bytes=1, cycles=2),         #CLC
    '38': Instr(method=Implide.imp_sec, bytes=1, cycles=2),         #SEC
    '58': Instr(method=Implide.imp_cli, bytes=1, cycles=2),         #CLI
    '78': Instr(method=Implide.imp_sei, bytes=1, cycles=2),         #SEI
    'B8': Instr(method=Implide.imp_clv, bytes=1, cycles=2),         #CLV
    'D8': Instr(method=Implide.imp_cld, bytes=1, cycles=2),         #CLD
    'F8': Instr(method=Implide.imp_sed, bytes=1, cycles=2),         #SED

    '9A': Instr(method=Implide.imp_txs, bytes=1, cycles=2),         #TXS
    'BA': Instr(method=Implide.imp_tsx, bytes=1, cycles=2),         #TSX
    '48': Instr(method=Implide.imp_pha, bytes=1, cycles=3),         #PHA
    '68': Instr(method=Implide.imp_pla, bytes=1, cycles=4),         #PLA
    '08': Instr(method=Implide.imp_php, bytes=1, cycles=3),         #PHP
    '28': Instr(method=Implide.imp_plp, bytes=1, cycles=4),         #PLP

    'AA': Instr(method=Implide.imp_tax, bytes=1, cycles=2),         #TAX
    '8A': Instr(method=Implide.imp_txa, bytes=1, cycles=2),         #TXA
    'CA': Instr(method=Implide.imp_dex, bytes=1, cycles=2),         #DEX
    'E8': Instr(method=Implide.imp_inx, bytes=1, cycles=2),         #INX
    'A8': Instr(method=Implide.imp_tay, bytes=1, cycles=2),         #TAY
    '98': Instr(method=Implide.imp_tya, bytes=1, cycles=2),         #TYA
    '88': Instr(method=Implide.imp_dey, bytes=1, cycles=2),         #DEY
    'C8': Instr(method=Implide.imp_iny, bytes=1, cycles=2)          #INY
}

# relative_opcodes = {
#     '10': ,                         #BPL
#     '30': ,                         #BMI
#     '50': ,                         #BVC
#     '70': ,                         #BVS
#     '90': ,                         #BCC
#     'B0': ,                         #BCS
#     'D0': ,                         #BNE
#     'F0': ,                         #BEQ
# }

# accumulator_opcodes = {
#     '0A': ,                         #ASL
#     '4A': ,                         #LSR
#     '2A': ,                         #ROL
#     '6A': ,                         #ROR
# }
