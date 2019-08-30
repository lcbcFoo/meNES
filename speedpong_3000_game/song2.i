song2_header:
    .db $01           ;1 stream

    .db SFX_1         ;which stream
    .db $01           ;status byte (stream enabled)
    .db SQUARE_1      ;which channel
    .db $70           ;duty (01)
    .db ve_battlekid_1b  ;volume envelope
    .dw song2_square2 ;pointer to stream
    .db $80           ;tempo


song2_square2:
    .db thirtysecond, Cs6, D5
    .db endsound
