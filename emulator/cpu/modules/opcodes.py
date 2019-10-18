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

# Instructions that need to add a cycle if page changes.
# check_page = [0x7D, 0x79, 0x71, 0x3D, 0x39, 0x31, 0xDD, 0xD9, 0xD1,
#               0x5D, 0x59, 0x51, 0xBD, 0xB9, 0xB1, 0xBE, 0xBC, 0x1D,
#               0x19, 0x11, 0xFD, 0xF9, 0xF1]

opcodes_dict = {
    # Immediate
    0x69: Instr(type='immediate', method=Immediate.imd_adc, bytes=2, cycles=2),   #ADC
    0x29: Instr(type='immediate', method=Immediate.imd_and, bytes=2, cycles=2),   #AND
    0xC9: Instr(type='immediate', method=Immediate.imd_cmp, bytes=2, cycles=2),   #CMP
    0xE0: Instr(type='immediate', method=Immediate.imd_cpx, bytes=2, cycles=2),   #CPX
    0xC0: Instr(type='immediate', method=Immediate.imd_cpy, bytes=2, cycles=2),   #CPY
    0x49: Instr(type='immediate', method=Immediate.imd_eor, bytes=2, cycles=2),   #EOR
    0xA9: Instr(type='immediate', method=Immediate.imd_lda, bytes=2, cycles=2),   #LDA
    0xA2: Instr(type='immediate', method=Immediate.imd_ldx, bytes=2, cycles=2),   #LDX
    0xA0: Instr(type='immediate', method=Immediate.imd_ldy, bytes=2, cycles=2),   #LDY
    0x09: Instr(type='immediate', method=Immediate.imd_ora, bytes=2, cycles=2),   #ORA
    0xE9: Instr(type='immediate', method=Immediate.imd_sbc, bytes=2, cycles=2),   #SBC

    # Zero page
    0x65: Instr(type='zeropage', method=ZeroPage.zp_adc, bytes=2, cycles=3),     #ADC
    0x25: Instr(type='zeropage', method=ZeroPage.zp_and, bytes=2, cycles=3),     #AND
    0x06: Instr(type='zeropage', method=ZeroPage.zp_asl, bytes=2, cycles=5),     #ASL
    0x24: Instr(type='zeropage', method=ZeroPage.zp_bit, bytes=2, cycles=3),     #BIT
    0xC5: Instr(type='zeropage', method=ZeroPage.zp_cmp, bytes=2, cycles=3),     #CMP
    0xE4: Instr(type='zeropage', method=ZeroPage.zp_cpx, bytes=2, cycles=3),     #CPX
    0xC4: Instr(type='zeropage', method=ZeroPage.zp_cpy, bytes=2, cycles=3),     #CPY
    0xC6: Instr(type='zeropage', method=ZeroPage.zp_dec, bytes=2, cycles=5),     #DEC
    0x45: Instr(type='zeropage', method=ZeroPage.zp_eor, bytes=2, cycles=3),     #EOR
    0xE6: Instr(type='zeropage', method=ZeroPage.zp_inc, bytes=2, cycles=5),     #INC
    0xA5: Instr(type='zeropage', method=ZeroPage.zp_lda, bytes=2, cycles=3),     #LDA
    0xA6: Instr(type='zeropage', method=ZeroPage.zp_ldx, bytes=2, cycles=3),     #LDX
    0xA4: Instr(type='zeropage', method=ZeroPage.zp_ldy, bytes=2, cycles=3),     #LDY
    0x46: Instr(type='zeropage', method=ZeroPage.zp_lsr, bytes=2, cycles=5),     #LSR
    0x05: Instr(type='zeropage', method=ZeroPage.zp_ora, bytes=2, cycles=3),     #ORA
    0x26: Instr(type='zeropage', method=ZeroPage.zp_rol, bytes=2, cycles=5),     #ROL
    0x66: Instr(type='zeropage', method=ZeroPage.zp_ror, bytes=2, cycles=5),     #ROR
    0xE5: Instr(type='zeropage', method=ZeroPage.zp_sbc, bytes=2, cycles=3),     #SBC
    0x85: Instr(type='zeropage', method=ZeroPage.zp_sta, bytes=2, cycles=3),     #STA
    0x86: Instr(type='zeropage', method=ZeroPage.zp_stx, bytes=2, cycles=3),     #STX
    0x84: Instr(type='zeropage', method=ZeroPage.zp_sty, bytes=2, cycles=3),     #STY

    # Zerop page X
    0xD6: Instr(type='zeropage', method=ZeroPage.zpx_dec, bytes=2, cycles=6),    #DEC
    0x55: Instr(type='zeropage', method=ZeroPage.zpx_eor, bytes=2, cycles=4),    #EOR
    0x75: Instr(type='zeropage', method=ZeroPage.zpx_adc, bytes=2, cycles=4),    #ADC
    0x35: Instr(type='zeropage', method=ZeroPage.zpx_and, bytes=2, cycles=4),    #AND
    0x16: Instr(type='zeropage', method=ZeroPage.zpx_asl, bytes=2, cycles=6),    #ASL
    0xD5: Instr(type='zeropage', method=ZeroPage.zpx_cmp, bytes=2, cycles=4),    #CMP
    0xF6: Instr(type='zeropage', method=ZeroPage.zpx_inc, bytes=2, cycles=6),    #INC
    0xB5: Instr(type='zeropage', method=ZeroPage.zpx_lda, bytes=2, cycles=4),    #LDA
    0xB4: Instr(type='zeropage', method=ZeroPage.zpx_ldy, bytes=2, cycles=4),    #LDY
    0x56: Instr(type='zeropage', method=ZeroPage.zpx_lsr, bytes=2, cycles=6),    #LSR
    0x15: Instr(type='zeropage', method=ZeroPage.zpx_ora, bytes=2, cycles=4),    #ORA
    0x36: Instr(type='zeropage', method=ZeroPage.zpx_rol, bytes=2, cycles=6),    #ROL
    0x76: Instr(type='zeropage', method=ZeroPage.zpx_ror, bytes=2, cycles=6),    #ROR
    0xF5: Instr(type='zeropage', method=ZeroPage.zpx_sbc, bytes=2, cycles=4),    #SBC
    0x95: Instr(type='zeropage', method=ZeroPage.zpx_sta, bytes=2, cycles=4),    #STA
    0x94: Instr(type='zeropage', method=ZeroPage.zpx_sty, bytes=2, cycles=4),    #STY

    # Zero page Y
    0xB6: Instr(type='zeropage', method=ZeroPage.zpy_ldx, bytes=2, cycles=4),    #LDX
    0x96: Instr(type='zeropage', method=ZeroPage.zpy_stx, bytes=2, cycles=4),    #STX

    # Absolute
    0x6D: Instr(type='absolute', method=Absolute.abs_adc, bytes=3, cycles=4),    #ADC
    0x2D: Instr(type='absolute', method=Absolute.abs_and, bytes=3, cycles=4),    #AND
    0x0E: Instr(type='absolute', method=Absolute.abs_asl, bytes=3, cycles=6),    #ASL
    0x2C: Instr(type='absolute', method=Absolute.abs_bit, bytes=3, cycles=4),    #BIT
    0xCD: Instr(type='absolute', method=Absolute.abs_cmp, bytes=3, cycles=4),    #CMP
    0xEC: Instr(type='absolute', method=Absolute.abs_cpx, bytes=3, cycles=4),    #CPX
    0xCC: Instr(type='absolute', method=Absolute.abs_cpy, bytes=3, cycles=4),    #CPY
    0xCE: Instr(type='absolute', method=Absolute.abs_dec, bytes=3, cycles=6),    #DEC
    0x4D: Instr(type='absolute', method=Absolute.abs_eor, bytes=3, cycles=4),    #EOR
    0xEE: Instr(type='absolute', method=Absolute.abs_inc, bytes=3, cycles=6),    #INC
    0x4C: Instr(type='absolute', method=Absolute.abs_jmp, bytes=3, cycles=3),    #JMP
    0x20: Instr(type='absolute', method=Absolute.abs_jsr, bytes=3, cycles=6),    #JSR
    0xAD: Instr(type='absolute', method=Absolute.abs_lda, bytes=3, cycles=4),    #LDA
    0xAE: Instr(type='absolute', method=Absolute.abs_ldx, bytes=3, cycles=4),    #LDX
    0xAC: Instr(type='absolute', method=Absolute.abs_ldy, bytes=3, cycles=4),    #LDY
    0x4E: Instr(type='absolute', method=Absolute.abs_lsr, bytes=3, cycles=6),    #LSR
    0x0D: Instr(type='absolute', method=Absolute.abs_ora, bytes=3, cycles=4),    #ORA
    0x2E: Instr(type='absolute', method=Absolute.abs_rol, bytes=3, cycles=6),    #ROL
    0x6E: Instr(type='absolute', method=Absolute.abs_ror, bytes=3, cycles=6),    #ROR
    0xED: Instr(type='absolute', method=Absolute.abs_sbc, bytes=3, cycles=4),    #SBC
    0x8D: Instr(type='absolute', method=Absolute.abs_sta, bytes=3, cycles=4),    #STA
    0x8E: Instr(type='absolute', method=Absolute.abs_stx, bytes=3, cycles=4),    #STX
    0x8C: Instr(type='absolute', method=Absolute.abs_sty, bytes=3, cycles=4),    #STY

    # Absolute X
    0x7D: Instr(type='absolute_x', method=Absolute.absX_adc, bytes=3, cycles=4),   #ADC
    0x3D: Instr(type='absolute_x', method=Absolute.absX_and, bytes=3, cycles=4),   #AND
    0x1E: Instr(type='absolute_x', method=Absolute.absX_asl, bytes=3, cycles=7),   #ASL
    0xDD: Instr(type='absolute_x', method=Absolute.absX_cmp, bytes=3, cycles=4),   #CMP
    0xDE: Instr(type='absolute_x', method=Absolute.absX_dec, bytes=3, cycles=7),   #DEC
    0x5D: Instr(type='absolute_x', method=Absolute.absX_eor, bytes=3, cycles=4),   #EOR
    0xFE: Instr(type='absolute_x', method=Absolute.absX_inc, bytes=3, cycles=7),   #INC
    0xBD: Instr(type='absolute_x', method=Absolute.absX_lda, bytes=3, cycles=4),   #LDA
    0xBC: Instr(type='absolute_x', method=Absolute.absX_ldy, bytes=3, cycles=4),   #LDY
    0x5E: Instr(type='absolute_x', method=Absolute.absX_lsr, bytes=3, cycles=7),   #LSR
    0x1D: Instr(type='absolute_x', method=Absolute.absX_ora, bytes=3, cycles=4),   #ORA
    0x3E: Instr(type='absolute_x', method=Absolute.absX_rol, bytes=3, cycles=7),   #ROL
    0x7E: Instr(type='absolute_x', method=Absolute.absX_ror, bytes=3, cycles=7),   #ROR
    0xFD: Instr(type='absolute_x', method=Absolute.absX_sbc, bytes=3, cycles=4),   #SBC
    0x9D: Instr(type='absolute_x', method=Absolute.absX_sta, bytes=3, cycles=5),   #STA

    # Absolute Y
    0x79: Instr(type='absolute_y', method=Absolute.absY_adc, bytes=3, cycles=4),   #ADC
    0x39: Instr(type='absolute_y', method=Absolute.absY_and, bytes=3, cycles=4),   #AND
    0xD9: Instr(type='absolute_y', method=Absolute.absY_cmp, bytes=3, cycles=4),   #CMP
    0x59: Instr(type='absolute_y', method=Absolute.absY_eor, bytes=3, cycles=4),   #EOR
    0xB9: Instr(type='absolute_y', method=Absolute.absY_lda, bytes=3, cycles=4),   #LDA
    0xBE: Instr(type='absolute_y', method=Absolute.absY_ldx, bytes=3, cycles=4),   #LDX
    0x19: Instr(type='absolute_y', method=Absolute.absY_ora, bytes=3, cycles=4),   #ORA
    0xF9: Instr(type='absolute_y', method=Absolute.absY_sbc, bytes=3, cycles=4),   #SBC
    0x99: Instr(type='absolute_y', method=Absolute.absY_sta, bytes=3, cycles=5),   #STA

    # Indirect
    0x6C: Instr(type='indirect', method=Indirect.ind_jmp, bytes=3, cycles=5),    #JMP

    # Indirect X
    0x61: Instr(type='indirect', method=Indirect.indx_adc, bytes=2, cycles=6),   #ADC
    0x21: Instr(type='indirect', method=Indirect.indx_and, bytes=2, cycles=6),   #AND
    0xC1: Instr(type='indirect', method=Indirect.indx_cmp, bytes=2, cycles=6),   #CMP
    0x41: Instr(type='indirect', method=Indirect.indx_eor, bytes=2, cycles=6),   #EOR
    0xA1: Instr(type='indirect', method=Indirect.indx_lda, bytes=2, cycles=6),   #LDA
    0x01: Instr(type='indirect', method=Indirect.indx_ora, bytes=2, cycles=6),   #ORA
    0xE1: Instr(type='indirect', method=Indirect.indx_sbc, bytes=2, cycles=6),   #SBC
    0x81: Instr(type='indirect', method=Indirect.indx_sta, bytes=2, cycles=6),   #STA

    # Indirect Y
    0x71: Instr(type='indirect', method=Indirect.indy_adc, bytes=2, cycles=5),   #ADC
    0x31: Instr(type='indirect', method=Indirect.indy_and, bytes=2, cycles=5),   #AND
    0xD1: Instr(type='indirect', method=Indirect.indy_cmp, bytes=2, cycles=5),   #CMP
    0x51: Instr(type='indirect', method=Indirect.indy_eor, bytes=2, cycles=5),   #EOR
    0xB1: Instr(type='indirect', method=Indirect.indy_lda, bytes=2, cycles=5),   #LDA
    0x11: Instr(type='indirect', method=Indirect.indy_ora, bytes=2, cycles=5),   #ORA
    0xF1: Instr(type='indirect', method=Indirect.indy_sbc, bytes=2, cycles=5),   #SBC
    0x91: Instr(type='indirect', method=Indirect.indy_sta, bytes=2, cycles=5),   #STA

    # Implied
    0x00: Instr(type='implied', method=Implied.imp_brk, bytes=1, cycles=7),     #BRK
    0xEA: Instr(type='implied', method=Implied.imp_nop, bytes=1, cycles=2),     #NOP
    0x40: Instr(type='implied', method=Implied.imp_rti, bytes=1, cycles=6),     #RTI
    0x60: Instr(type='implied', method=Implied.imp_rts, bytes=1, cycles=6),     #RTS

    0x18: Instr(type='implied', method=Implied.imp_clc, bytes=1, cycles=2),     #CLC
    0x38: Instr(type='implied', method=Implied.imp_sec, bytes=1, cycles=2),     #SEC
    0x58: Instr(type='implied', method=Implied.imp_cli, bytes=1, cycles=2),     #CLI
    0x78: Instr(type='implied', method=Implied.imp_sei, bytes=1, cycles=2),     #SEI
    0xB8: Instr(type='implied', method=Implied.imp_clv, bytes=1, cycles=2),     #CLV
    0xD8: Instr(type='implied', method=Implied.imp_cld, bytes=1, cycles=2),     #CLD
    0xF8: Instr(type='implied', method=Implied.imp_sed, bytes=1, cycles=2),     #SED

    0x9A: Instr(type='implied', method=Implied.imp_txs, bytes=1, cycles=2),     #TXS
    0xBA: Instr(type='implied', method=Implied.imp_tsx, bytes=1, cycles=2),     #TSX
    0x48: Instr(type='implied', method=Implied.imp_pha, bytes=1, cycles=3),     #PHA
    0x68: Instr(type='implied', method=Implied.imp_pla, bytes=1, cycles=4),     #PLA
    0x08: Instr(type='implied', method=Implied.imp_php, bytes=1, cycles=3),     #PHP
    0x28: Instr(type='implied', method=Implied.imp_plp, bytes=1, cycles=4),     #PLP

    0xAA: Instr(type='implied', method=Implied.imp_tax, bytes=1, cycles=2),     #TAX
    0x8A: Instr(type='implied', method=Implied.imp_txa, bytes=1, cycles=2),     #TXA
    0xCA: Instr(type='implied', method=Implied.imp_dex, bytes=1, cycles=2),     #DEX
    0xE8: Instr(type='implied', method=Implied.imp_inx, bytes=1, cycles=2),     #INX
    0xA8: Instr(type='implied', method=Implied.imp_tay, bytes=1, cycles=2),     #TAY
    0x98: Instr(type='implied', method=Implied.imp_tya, bytes=1, cycles=2),     #TYA
    0x88: Instr(type='implied', method=Implied.imp_dey, bytes=1, cycles=2),     #DEY
    0xC8: Instr(type='implied', method=Implied.imp_iny, bytes=1, cycles=2),     #INY

    # Relative
    0x10: Instr(type='relative', method=Relative.rel_bpl, bytes=2, cycles=2),   #BPL
    0x30: Instr(type='relative', method=Relative.rel_bmi, bytes=2, cycles=2),   #BMI
    0x50: Instr(type='relative', method=Relative.rel_bvc, bytes=2, cycles=2),   #BVC
    0x70: Instr(type='relative', method=Relative.rel_bvs, bytes=2, cycles=2),   #BVS
    0x90: Instr(type='relative', method=Relative.rel_bcc, bytes=2, cycles=2),   #BCC
    0xB0: Instr(type='relative', method=Relative.rel_bcs, bytes=2, cycles=2),   #BCS
    0xD0: Instr(type='relative', method=Relative.rel_bne, bytes=2, cycles=2),   #BNE
    0xF0: Instr(type='relative', method=Relative.rel_beq, bytes=2, cycles=2),   #BEQ

    # Accumulator
    0x0A: Instr(type='accumulator', method=Accumulator.acc_asl, bytes=1, cycles=2),   #ASL
    0x4A: Instr(type='accumulator', method=Accumulator.acc_lsr, bytes=1, cycles=2),   #LSR
    0x2A: Instr(type='accumulator', method=Accumulator.acc_rol, bytes=1, cycles=2),   #ROL
    0x6A: Instr(type='accumulator', method=Accumulator.acc_ror, bytes=1, cycles=2),   #ROR

}
