;silence song.  disables all streams

song0_header:
    .db $04           ;4 streams

    .db MUSIC_SQ1     ;which stream
    .db $01           ;status byte (stream enabled)
    .db SQUARE_1      ;which channel
    .db $BC           ;initial volume (C) and duty (10)
    .dw song0_square1 ;pointer to stream

    .db MUSIC_SQ2     ;which stream
    .db $01           ;status byte (stream enabled)
    .db SQUARE_2      ;which channel
    .db $38           ;initial volume (8) and duty (00)
    .dw song0_square2 ;pointer to stream

    .db MUSIC_TRI     ;which stream
    .db $01           ;status byte (stream enabled)
    .db TRIANGLE      ;which channel
    .db $81           ;initial volume (on)
    .dw song0_tri     ;pointer to stream

    .db MUSIC_NOI     ;which stream
    .db $00           ;disabled.  We will have our load routine skip the
                        ;   rest of the reads if the status byte disables the stream.
                        ;   We are disabling Noise because we haven't covered it yet.

;these are the actual data streams that are pointed to in our stream headers.
song0_square1:
    .db A3, C4, E4, A4, C5, E5, A5 ;some notes.  A minor

song0_square2:
    .db A3, A3, A3, E4, A3, A3, E4 ;some notes to play on square 2

song0_tri:
    .db A3, A3, A3, A3, A3, A3, A3 ;triangle data
