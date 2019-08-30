song3_header:
    .db $01           ;1 stream

    .db SFX_2         ;which stream
    .db $01           ;status byte (stream enabled)
    .db SQUARE_1      ;which channel
    .db $70           ;duty (01)
    .db ve_battlekid_1b  ;volume envelope
    .dw song3_square2 ;pointer to stream
    .db $80           ;tempo


song3_square2:
    .db eighth, C3, D3, E3, quarter, G3, eighth, E3, half, G3
    .db endsound
