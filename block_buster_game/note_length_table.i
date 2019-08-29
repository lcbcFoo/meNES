;note length constants (aliases)
thirtysecond = $80
sixteenth = $81
eighth = $82
quarter = $83
half = $84
whole = $85
d_sixteenth = $86
d_eighth = $87
d_quarter = $88
d_half = $89
d_whole = $8A   ;don't forget we are counting in hex
t_quarter = $8B
five_eighths = $8C
five_sixteenths = $8D

note_length_table:
    .db $01   ;32nd note
    .db $02   ;16th note
    .db $04   ;8th note
    .db $08   ;quarter note
    .db $10   ;half note
    .db $20   ;whole note
              ;---dotted notes
    .db $03   ;dotted 16th note
    .db $06   ;dotted 8th note
    .db $0C   ;dotted quarter note
    .db $18   ;dotted half note
    .db $30   ;dotted whole note?

  	;; Other
  	;; Modified quarter to fit after d_sixtength triplets
  	.db	$07
  	.db	$14		; 2 quarters plus an 8th
  	.db	$0a
