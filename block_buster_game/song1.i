song1_header:
    .db $04           ;4 streams

    .db MUSIC_SQ1     ;which stream
    .db $01           ;status byte (stream enabled)
    .db SQUARE_1      ;which channel
    .db $70           ;initial duty (01)
    .db ve_tgl_1      ;volume envelope
    .dw song1_square1 ;pointer to stream
    .db $53           ;tempo

    .db MUSIC_SQ2     ;which stream
    .db $01           ;status byte (stream enabled)
    .db SQUARE_2      ;which channel
    .db $B0           ;initial duty (10)
    .db ve_tgl_2      ;volume envelope
    .dw song1_square2 ;pointer to stream
    .db $53           ;tempo

    .db MUSIC_TRI     ;which stream
    .db $01           ;status byte (stream enabled)
    .db TRIANGLE      ;which channel
    .db $80           ;initial volume (on)
    .db ve_tgl_2      ;volume envelope
    .dw song1_tri     ;pointer to stream
    .db $53           ;tempo

    .db MUSIC_NOI     ;which stream
    .db $01           ;enabled
    .db NOISE
    .db $30           ;initial duty_vol
    .db ve_drum_decay ;volume envelope
    .dw song1_noise   ;pointer to stream
    .db $53           ;tempo


song1_square1:
    .db eighth
    .db set_loop1_counter, 14             ;repeat 14 times
s1s1loop:
    .db A2, A2, A2, A3, A2, A3, A2, A3
    .db transpose                         ;the transpose opcode take a 2-byte argument
    .dw s1lookup_table                     ;which is the address of the lookup table

    .db loop1                             ;finite loop (14 times)
    .dw s1s1loop

    .db loop                              ;infinite loop
    .dw song1_square1

s1lookup_table:
    .db 2, -1, -1, -1, -1, -1, -2
    .db -1, -1, 0, -1, 8, -8, 8       ;14 entries long, reverse order



song1_square2:
    .db sixteenth
    .db rest    ;offset for delay effect
    .db eighth
s1s2loop_point:
    .db rest
    .db A4, C5, B4, C5, A4, C5, B4, C5
    .db A4, C5, B4, C5, A4, C5, B4, C5
    .db A4, C5, B4, C5, A4, C5, B4, C5
    .db A4, C5, B4, C5, A4, C5, B4, C5
    .db Ab4, B4, A4, B4, Ab4, B4, A4, B4
    .db B4, E5, D5, E5, B4, E5, D5, E5
    .db A4, Eb5, C5, Eb5, A4, Eb5, C5, Eb5
    .db A4, D5, Db5, D5, A4, D5, Db5, D5
    .db A4, C5, F5, A5, C6, A5, F5, C5
    .db Gb4, B4, Eb5, Gb5, B5, Gb5, Eb5, B4
    .db F4, Bb4, D5, F5, Gs5, F5, D5, As4
    .db E4, A4, Cs5, E5, A5, E5, sixteenth, Cs5, rest
    .db eighth
    .db Ds4, Gs4, C5, Ds5, Gs5, Ds5, C5, Gs4
    .db sixteenth
    .db G4, Fs4, G4, Fs4, G4, Fs4, G4, Fs4
    .db eighth
    .db G4, B4, D5, G5
    .db loop
    .dw s1s2loop_point

song1_tri:
    .db eighth
    .db A5, C6, B5, C6, A5, C6, B5, C6 ;triangle data
    .db A5, C6, B5, C6, A5, C6, B5, C6
    .db A5, C6, B5, C6, A5, C6, B5, C6
    .db A5, C6, B5, C6, A5, C6, B5, C6
    .db Ab5, B5, A5, B5, Ab5, B5, A5, B5
    .db B5, E6, D6, E6, B5, E6, D6, E6
    .db A5, Eb6, C6, Eb6, A5, Eb6, C6, Eb6
    .db A5, D6, Db6, D6, A5, D6, Db6, D6
    .db A5, C6, F6, A6, C7, A6, F6, C6
    .db Gb5, B5, Eb6, Gb6, B6, Gb6, Eb6, B5
    .db F5, Bb5, D6, F6, Gs6, F6, D6, As5
    .db E5, A5, Cs6, E6, A6, E6, Cs6, A5
    .db Ds5, Gs5, C6, Ds6, Gs6, Ds6, C6, Gs5
    .db sixteenth
    .db G5, Fs5, G5, Fs5, G5, Fs5, G5, Fs5
    .db G5, B5, D6, G6, B5, D6, B6, D7
    .db loop
    .dw song1_tri

song1_noise:
    .db eighth, $04
    .db sixteenth, $04, $04, $04
    .db d_eighth, $04
    .db sixteenth, $04, $04, $04, $04
    .db eighth, $04, $04
    .db loop
    .dw song1_noise
