song2_header:
    .byte $01           ;1 stream

    .byte SFX_1         ;which stream
    .byte $01           ;status byte (stream enabled)
    .byte SQUARE_1      ;which channel
    .byte $70           ;duty (01)
    .byte ve_battlekid_1b  ;volume envelope
    .word song2_square2 ;pointer to stream
    .byte $80           ;tempo


song2_square2:
    .byte thirtysecond, Cs6, D5
    .byte endsound
