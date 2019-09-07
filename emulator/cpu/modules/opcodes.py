
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
    '65': ,                         #ADC
    '25': ,                         #AND
    '06': ,                         #ASL
    '24': ,                         #BIT
    'C5': ,                         #CMP
    'E4': ,                         #CPX
    'C4': ,                         #CPY
    'C6': ,                         #DEC
    '45': ,                         #EOR
    'E6': ,                         #INC
    'A5': ,                         #LDA
    'A6': ,                         #LDX
    'A4': ,                         #LDY
    '46': ,                         #LSR
    '05': ,                         #ORA
    '26': ,                         #ROL
    '66': ,                         #ROR
    'E5': ,                         #SBC
    '85': ,                         #STA
    '86': ,                         #STX
    '84': ,                         #STY
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