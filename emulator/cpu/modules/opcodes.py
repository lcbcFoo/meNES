# Dict structure:
# {"opc": Instr(type=instruction_type, method=class_name.method_name(oper), bytes=, cycles=)}

from collections import namedtuple

from cpu.modules.zero_page import ZeroPage
from cpu.modules.absolute import Absolute
from cpu.modules.immediate import Immediate
from cpu.modules.implied import Implied
from cpu.modules.indirect import Indirect
from cpu.modules.accumulator import Accumulator
from cpu.modules.relative import Relative

Instr = namedtuple('Instr', 'type method bytes cycles')


opcodes_dict = {
    # Immediate
    '69': Instr(type='immediate', method=Immediate.imd_adc, bytes=2, cycles=2),   #ADC
    '29': Instr(type='immediate', method=Immediate.imd_and, bytes=2, cycles=2),   #AND
    'C9': Instr(type='immediate', method=Immediate.imd_cmp, bytes=2, cycles=2),   #CMP
    'E0': Instr(type='immediate', method=Immediate.imd_cpx, bytes=2, cycles=2),   #CPX
    'C0': Instr(type='immediate', method=Immediate.imd_cpy, bytes=2, cycles=2),   #CPY
    '49': Instr(type='immediate', method=Immediate.imd_eor, bytes=2, cycles=2),   #EOR
    'A9': Instr(type='immediate', method=Immediate.imd_lda, bytes=2, cycles=2),   #LDA
    'A2': Instr(type='immediate', method=Immediate.imd_ldx, bytes=2, cycles=2),   #LDX
    'A0': Instr(type='immediate', method=Immediate.imd_ldy, bytes=2, cycles=2),   #LDY
    '09': Instr(type='immediate', method=Immediate.imd_ora, bytes=2, cycles=2),   #ORA
    'E9': Instr(type='immediate', method=Immediate.imd_sbc, bytes=2, cycles=2),   #SBC

    # Zero page
    '65': Instr(type='zeropage', method=ZeroPage.zp_adc, bytes=2, cycles=3),     #ADC
    '25': Instr(type='zeropage', method=ZeroPage.zp_and, bytes=2, cycles=3),     #AND
    '06': Instr(type='zeropage', method=ZeroPage.zp_asl, bytes=2, cycles=5),     #ASL
    '24': Instr(type='zeropage', method=ZeroPage.zp_bit, bytes=2, cycles=3),     #BIT
    'C5': Instr(type='zeropage', method=ZeroPage.zp_cmp, bytes=2, cycles=3),     #CMP
    'E4': Instr(type='zeropage', method=ZeroPage.zp_cpx, bytes=2, cycles=3),     #CPX
    'C4': Instr(type='zeropage', method=ZeroPage.zp_cpy, bytes=2, cycles=3),     #CPY
    'C6': Instr(type='zeropage', method=ZeroPage.zp_dec, bytes=2, cycles=5),     #DEC
    '45': Instr(type='zeropage', method=ZeroPage.zp_eor, bytes=2, cycles=3),     #EOR
    'E6': Instr(type='zeropage', method=ZeroPage.zp_inc, bytes=2, cycles=5),     #INC
    'A5': Instr(type='zeropage', method=ZeroPage.zp_lda, bytes=2, cycles=3),     #LDA
    'A6': Instr(type='zeropage', method=ZeroPage.zp_ldx, bytes=2, cycles=3),     #LDX
    'A4': Instr(type='zeropage', method=ZeroPage.zp_ldy, bytes=2, cycles=3),     #LDY
    '46': Instr(type='zeropage', method=ZeroPage.zp_lsr, bytes=2, cycles=5),     #LSR
    '05': Instr(type='zeropage', method=ZeroPage.zp_ora, bytes=2, cycles=3),     #ORA
    '26': Instr(type='zeropage', method=ZeroPage.zp_rol, bytes=2, cycles=5),     #ROL
    '66': Instr(type='zeropage', method=ZeroPage.zp_ror, bytes=2, cycles=5),     #ROR
    'E5': Instr(type='zeropage', method=ZeroPage.zp_sbc, bytes=2, cycles=3),     #SBC
    '85': Instr(type='zeropage', method=ZeroPage.zp_sta, bytes=2, cycles=3),     #STA
    '86': Instr(type='zeropage', method=ZeroPage.zp_stx, bytes=2, cycles=3),     #STX
    '84': Instr(type='zeropage', method=ZeroPage.zp_sty, bytes=2, cycles=3),     #STY

    # Zerop page X
    'D6': Instr(type='zeropage', method=ZeroPage.zpx_dec, bytes=2, cycles=6),    #DEC
    '55': Instr(type='zeropage', method=ZeroPage.zpx_eor, bytes=2, cycles=4),    #EOR
    '75': Instr(type='zeropage', method=ZeroPage.zpx_adc, bytes=2, cycles=4),    #ADC
    '35': Instr(type='zeropage', method=ZeroPage.zpx_and, bytes=2, cycles=4),    #AND
    '16': Instr(type='zeropage', method=ZeroPage.zpx_asl, bytes=2, cycles=6),    #ASL
    'D5': Instr(type='zeropage', method=ZeroPage.zpx_cmp, bytes=2, cycles=4),    #CMP
    'F6': Instr(type='zeropage', method=ZeroPage.zpx_inc, bytes=2, cycles=6),    #INC
    'B5': Instr(type='zeropage', method=ZeroPage.zpx_lda, bytes=2, cycles=4),    #LDA
    'B4': Instr(type='zeropage', method=ZeroPage.zpx_ldy, bytes=2, cycles=4),    #LDY
    '56': Instr(type='zeropage', method=ZeroPage.zpx_lsr, bytes=2, cycles=6),    #LSR
    '15': Instr(type='zeropage', method=ZeroPage.zpx_ora, bytes=2, cycles=4),    #ORA
    '36': Instr(type='zeropage', method=ZeroPage.zpx_rol, bytes=2, cycles=6),    #ROL
    '76': Instr(type='zeropage', method=ZeroPage.zpx_ror, bytes=2, cycles=6),    #ROR
    'F5': Instr(type='zeropage', method=ZeroPage.zpx_sbc, bytes=2, cycles=4),    #SBC
    '95': Instr(type='zeropage', method=ZeroPage.zpx_sta, bytes=2, cycles=4),    #STA
    '94': Instr(type='zeropage', method=ZeroPage.zpx_sty, bytes=2, cycles=4),    #STY

    # Zero page Y
    'B6': Instr(type='zeropage', method=ZeroPage.zpy_ldx, bytes=2, cycles=4),    #LDX
    '96': Instr(type='zeropage', method=ZeroPage.zpy_stx, bytes=2, cycles=4),    #STX

    # Absolute
    '6D': Instr(type='absolute', method=Absolute.abs_adc, bytes=3, cycles=4),    #ADC
    '2D': Instr(type='absolute', method=Absolute.abs_and, bytes=3, cycles=4),    #AND
    '0E': Instr(type='absolute', method=Absolute.abs_asl, bytes=3, cycles=6),    #ASL
    '2C': Instr(type='absolute', method=Absolute.abs_bit, bytes=3, cycles=4),    #BIT
    'CD': Instr(type='absolute', method=Absolute.abs_cmp, bytes=3, cycles=4),    #CMP
    'EC': Instr(type='absolute', method=Absolute.abs_cpx, bytes=3, cycles=4),    #CPX
    'CC': Instr(type='absolute', method=Absolute.abs_cpy, bytes=3, cycles=4),    #CPY
    'CE': Instr(type='absolute', method=Absolute.abs_dec, bytes=3, cycles=6),    #DEC
    '4D': Instr(type='absolute', method=Absolute.abs_eor, bytes=3, cycles=4),    #EOR
    'EE': Instr(type='absolute', method=Absolute.abs_inc, bytes=3, cycles=6),    #INC
    '4C': Instr(type='absolute', method=Absolute.abs_jmp, bytes=3, cycles=3),    #JMP
    '20': Instr(type='absolute', method=Absolute.abs_jsr, bytes=3, cycles=6),    #JSR
    'AD': Instr(type='absolute', method=Absolute.abs_lda, bytes=3, cycles=4),    #LDA
    'AE': Instr(type='absolute', method=Absolute.abs_ldx, bytes=3, cycles=4),    #LDX
    'AC': Instr(type='absolute', method=Absolute.abs_ldy, bytes=3, cycles=4),    #LDY
    '4E': Instr(type='absolute', method=Absolute.abs_lsr, bytes=3, cycles=6),    #LSR
    '0D': Instr(type='absolute', method=Absolute.abs_ora, bytes=3, cycles=4),    #ORA
    '2E': Instr(type='absolute', method=Absolute.abs_rol, bytes=3, cycles=6),    #ROL
    '6E': Instr(type='absolute', method=Absolute.abs_ror, bytes=3, cycles=6),    #ROR
    'ED': Instr(type='absolute', method=Absolute.abs_sbc, bytes=3, cycles=4),    #SBC
    '8D': Instr(type='absolute', method=Absolute.abs_sta, bytes=3, cycles=4),    #STA
    '8E': Instr(type='absolute', method=Absolute.abs_stx, bytes=3, cycles=4),    #STX
    '8C': Instr(type='absolute', method=Absolute.abs_sty, bytes=3, cycles=4),    #STY

    # Absolute X
    '7D': Instr(type='absolute', method=Absolute.absX_adc, bytes=3, cycles=4),   #ADC
    '3D': Instr(type='absolute', method=Absolute.absX_and, bytes=3, cycles=4),   #AND
    '1E': Instr(type='absolute', method=Absolute.absX_asl, bytes=3, cycles=7),   #ASL
    'DD': Instr(type='absolute', method=Absolute.absX_cmp, bytes=3, cycles=4),   #CMP
    'DE': Instr(type='absolute', method=Absolute.absX_dec, bytes=3, cycles=7),   #DEC
    '5D': Instr(type='absolute', method=Absolute.absX_eor, bytes=3, cycles=4),   #EOR
    'FE': Instr(type='absolute', method=Absolute.absX_inc, bytes=3, cycles=7),   #INC
    'BD': Instr(type='absolute', method=Absolute.absX_lda, bytes=3, cycles=4),   #LDA
    'BC': Instr(type='absolute', method=Absolute.absX_ldy, bytes=3, cycles=4),   #LDY
    '5E': Instr(type='absolute', method=Absolute.absX_lsr, bytes=3, cycles=7),   #LSR
    '1D': Instr(type='absolute', method=Absolute.absX_ora, bytes=3, cycles=4),   #ORA
    '3E': Instr(type='absolute', method=Absolute.absX_rol, bytes=3, cycles=7),   #ROL
    '7E': Instr(type='absolute', method=Absolute.absX_ror, bytes=3, cycles=7),   #ROR
    'FD': Instr(type='absolute', method=Absolute.absX_sbc, bytes=3, cycles=4),   #SBC
    '9D': Instr(type='absolute', method=Absolute.absX_sta, bytes=3, cycles=5),   #STA

    # Absolute Y
    '79': Instr(type='absolute', method=Absolute.absY_adc, bytes=3, cycles=4),   #ADC
    '39': Instr(type='absolute', method=Absolute.absY_and, bytes=3, cycles=4),   #AND
    'D9': Instr(type='absolute', method=Absolute.absY_cmp, bytes=3, cycles=4),   #CMP
    '59': Instr(type='absolute', method=Absolute.absY_eor, bytes=3, cycles=4),   #EOR
    'B9': Instr(type='absolute', method=Absolute.absY_lda, bytes=3, cycles=4),   #LDA
    'BE': Instr(type='absolute', method=Absolute.absY_ldx, bytes=3, cycles=4),   #LDX
    '19': Instr(type='absolute', method=Absolute.absY_ora, bytes=3, cycles=4),   #ORA
    'F9': Instr(type='absolute', method=Absolute.absY_sbc, bytes=3, cycles=4),   #SBC
    '99': Instr(type='absolute', method=Absolute.absY_sta, bytes=3, cycles=5),   #STA

    # Indirect
    '6C': Instr(type='indirect', method=Indirect.ind_jmp, bytes=3, cycles=5),    #JMP

    # Indirect X
    '61': Instr(type='indirect', method=Indirect.indx_adc, bytes=2, cycles=6),   #ADC
    '21': Instr(type='indirect', method=Indirect.indx_and, bytes=2, cycles=6),   #AND
    'C1': Instr(type='indirect', method=Indirect.indx_cmp, bytes=2, cycles=6),   #CMP
    '41': Instr(type='indirect', method=Indirect.indx_eor, bytes=2, cycles=6),   #EOR
    'A1': Instr(type='indirect', method=Indirect.indx_lda, bytes=2, cycles=6),   #LDA
    '01': Instr(type='indirect', method=Indirect.indx_ora, bytes=2, cycles=6),   #ORA
    'E1': Instr(type='indirect', method=Indirect.indx_sbc, bytes=2, cycles=6),   #SBC
    '81': Instr(type='indirect', method=Indirect.indx_sta, bytes=2, cycles=6),   #STA

    # Indirect Y
    '71': Instr(type='indirect', method=Indirect.indy_adc, bytes=2, cycles=5),   #ADC
    '31': Instr(type='indirect', method=Indirect.indy_and, bytes=2, cycles=5),   #AND
    'D1': Instr(type='indirect', method=Indirect.indy_cmp, bytes=2, cycles=5),   #CMP
    '51': Instr(type='indirect', method=Indirect.indy_eor, bytes=2, cycles=5),   #EOR
    'B1': Instr(type='indirect', method=Indirect.indy_lda, bytes=2, cycles=5),   #LDA
    '11': Instr(type='indirect', method=Indirect.indy_ora, bytes=2, cycles=5),   #ORA
    'F1': Instr(type='indirect', method=Indirect.indy_sbc, bytes=2, cycles=5),   #SBC
    '91': Instr(type='indirect', method=Indirect.indy_sta, bytes=2, cycles=5),   #STA

    # Implied
    '00': Instr(type='implied', method=Implied.imp_brk, bytes=1, cycles=7),     #BRK
    'EA': Instr(type='implied', method=Implied.imp_nop, bytes=1, cycles=2),     #NOP
    '40': Instr(type='implied', method=Implied.imp_rti, bytes=1, cycles=6),     #RTI
    '60': Instr(type='implied', method=Implied.imp_rts, bytes=1, cycles=6),     #RTS

    '18': Instr(type='implied', method=Implied.imp_clc, bytes=1, cycles=2),     #CLC
    '38': Instr(type='implied', method=Implied.imp_sec, bytes=1, cycles=2),     #SEC
    '58': Instr(type='implied', method=Implied.imp_cli, bytes=1, cycles=2),     #CLI
    '78': Instr(type='implied', method=Implied.imp_sei, bytes=1, cycles=2),     #SEI
    'B8': Instr(type='implied', method=Implied.imp_clv, bytes=1, cycles=2),     #CLV
    'D8': Instr(type='implied', method=Implied.imp_cld, bytes=1, cycles=2),     #CLD
    'F8': Instr(type='implied', method=Implied.imp_sed, bytes=1, cycles=2),     #SED

    '9A': Instr(type='implied', method=Implied.imp_txs, bytes=1, cycles=2),     #TXS
    'BA': Instr(type='implied', method=Implied.imp_tsx, bytes=1, cycles=2),     #TSX
    '48': Instr(type='implied', method=Implied.imp_pha, bytes=1, cycles=3),     #PHA
    '68': Instr(type='implied', method=Implied.imp_pla, bytes=1, cycles=4),     #PLA
    '08': Instr(type='implied', method=Implied.imp_php, bytes=1, cycles=3),     #PHP
    '28': Instr(type='implied', method=Implied.imp_plp, bytes=1, cycles=4),     #PLP

    'AA': Instr(type='implied', method=Implied.imp_tax, bytes=1, cycles=2),     #TAX
    '8A': Instr(type='implied', method=Implied.imp_txa, bytes=1, cycles=2),     #TXA
    'CA': Instr(type='implied', method=Implied.imp_dex, bytes=1, cycles=2),     #DEX
    'E8': Instr(type='implied', method=Implied.imp_inx, bytes=1, cycles=2),     #INX
    'A8': Instr(type='implied', method=Implied.imp_tay, bytes=1, cycles=2),     #TAY
    '98': Instr(type='implied', method=Implied.imp_tya, bytes=1, cycles=2),     #TYA
    '88': Instr(type='implied', method=Implied.imp_dey, bytes=1, cycles=2),     #DEY
    'C8': Instr(type='implied', method=Implied.imp_iny, bytes=1, cycles=2),     #INY

    # Relative
    '10': Instr(type='relative', method=Relative.rel_bpl, bytes=2, cycles=2),   #BPL
    '30': Instr(type='relative', method=Relative.rel_bmi, bytes=2, cycles=2),   #BMI
    '50': Instr(type='relative', method=Relative.rel_bvc, bytes=2, cycles=2),   #BVC
    '70': Instr(type='relative', method=Relative.rel_bvs, bytes=2, cycles=2),   #BVS
    '90': Instr(type='relative', method=Relative.rel_bcc, bytes=2, cycles=2),   #BCC
    'B0': Instr(type='relative', method=Relative.rel_bcs, bytes=2, cycles=2),   #BCS
    'D0': Instr(type='relative', method=Relative.rel_bne, bytes=2, cycles=2),   #BNE
    'F0': Instr(type='relative', method=Relative.rel_beq, bytes=2, cycles=2),   #BEQ

    # Accumulator
    '0A': Instr(type='accumulator', method=Accumulator.acc_asl, bytes=1, cycles=2),   #ASL
    '4A': Instr(type='accumulator', method=Accumulator.acc_lsr, bytes=1, cycles=2),   #LSR
    '2A': Instr(type='accumulator', method=Accumulator.acc_rol, bytes=1, cycles=2),   #ROL
    '6A': Instr(type='accumulator', method=Accumulator.acc_ror, bytes=1, cycles=2),   #ROR

}
