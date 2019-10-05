; Author: tokumaru
; http://forums.nesdev.com/viewtopic.php?%20p=58138#58138
;----------------------------------------------------------------
; constants
;----------------------------------------------------------------
PRG_COUNT = 1 ;1 = 16KB, 2 = 32KB
MIRRORING = %0001 ;%0000 = horizontal, %0001 = vertical, %1000 = four-screen

;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000
   tmp .dsb 1
   ;NOTE: declare variables using the DSB and DSW directives, like this:

   ;MyVariable0 .dsb 1
   ;MyVariable1 .dsb 3

   .ende

   ;NOTE: you can also split the variable declarations into individual pages, like this:

   ;.enum $0100
   ;.ende

   ;.enum $0200
   ;.ende

;----------------------------------------------------------------
; iNES header
;----------------------------------------------------------------

   .db "NES", $1a ;identification of the iNES header
   .db PRG_COUNT ;number of 16KB PRG-ROM pages
   .db $01 ;number of 8KB CHR-ROM pages
   .db $00|MIRRORING ;mapper 0 and mirroring
   .dsb 9, $00 ;clear the remaining bytes

;----------------------------------------------------------------
; program bank(s)
;----------------------------------------------------------------

   .base $10000-(PRG_COUNT*$4000)


Reset:
   lda #10
   jsr fib
   brk ; Abort execution

NMI:

   ;NOTE: NMI code goes here

IRQ:

   ;NOTE: IRQ code goes here

.org $D000
fib:
    cmp #1
    beq case_base
    cmp #2
    beq case_base

    ; return fib(n-1) + fib(n-2)
    sec
    sbc #1
    
    ; call fib(n-1)
    pha
    jsr fib

    ; fib(n-1) => X
    tax
    
    ; restore n-1 to A
    pla

    ; n-1 => Y
    tay

    ; fib(n-1) => A
    txa
    pha
    tya

    ; n - 1 => A
    sec
    sbc #1

    ; call fib(n-2)
    jsr fib

    ; tmp = fib(n-2)
    sta tmp

    ; A = fib(n-1)
    pla
    clc
    adc tmp

    rts

case_base:
    lda #1
    rts
;----------------------------------------------------------------
; interrupt vectors
;----------------------------------------------------------------

   .org $fffa

   .dw NMI
   .dw Reset
   .dw IRQ
