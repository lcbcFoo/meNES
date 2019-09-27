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

   .enum $0500

   ;NOTE: declare variables using the DSB and DSW directives, like this:

   test_variable .dsb 1

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

;Increments once test variable, loads into acc
;increments once again the variable and adds it with acc
; the operation (2+1) should store 3 into acc
Reset:
   ; Test reg_a = 5
   lda #05
   ; Test store 5 on $0499
   sta $0499
   ; Test reg_a = 3
   lda #03
   ; Test reg_x = 2
   ldy #02
   ; Test reg_a = 5 + 3 = 8
   adc $0497, Y

   ; Test reg_a = 81
   lda #81
   sta $0516
   ; Test reg_a = 81 + 8 = 89
   adc $0514, Y
   brk ; Abort execution

   
    


NMI:

   ;NOTE: NMI code goes here

IRQ:

   ;NOTE: IRQ code goes here

;----------------------------------------------------------------
; interrupt vectors
;----------------------------------------------------------------

   .org $fffa

   .dw NMI
   .dw Reset
   .dw IRQ
