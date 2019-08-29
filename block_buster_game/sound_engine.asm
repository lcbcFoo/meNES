;----------------------------------------------------------------
; SOUND ENGINE CONSTANTS
;----------------------------------------------------------------

SQUARE_1 = $00 ;these are channel constants
SQUARE_2 = $01
TRIANGLE = $02
NOISE = $03

MUSIC_SQ1 = $00 ;these are stream number constants
MUSIC_SQ2 = $01 ;stream number is used to index into stream variables (see below)
MUSIC_TRI = $02
MUSIC_NOI = $03
SFX_1     = $04
SFX_2     = $05

;----------------------------------------------------------------
; SOUND ENGINE VARIABLES
;----------------------------------------------------------------
    .enum $0300    ;put variables starting at 0300

    sound_disable_flag .dsb 1 ;sound_disable_flag  .rs 1   ;a flag variable that keeps track of whether the sound engine is disabled or not.
    sound_temp1 .dsb 1 ;sound_temp1 .rs 1           ;temporary variables
    sound_temp2 .dsb 1 ;sound_temp2 .rs 1
    sound_sq1_old .dsb 1  ;the last value written to $4003
    sound_sq2_old .dsb 1  ;the last value written to $4007

    soft_apu_ports .dsb 16


    ;reserve 6 bytes, one for each stream
    stream_curr_sound .dsb 6 ;stream_curr_sound .rs 6     ;current song/sfx loaded
    stream_status .dsb 6 ;stream_status .rs 6         ;status byte.   bit0: (1: stream enabled; 0: stream disabled)
    stream_channel .dsb 6 ;stream_channel .rs 6        ;what channel is this stream playing on?
    stream_vol_duty .dsb 6 ;stream_vol_duty .rs 6       ;stream volume/duty settings
    stream_ptr_LO .dsb 6 ;stream_ptr_LO .rs 6         ;low byte of pointer to data stream
    stream_ptr_HI .dsb 6 ;stream_ptr_HI .rs 6         ;high byte of pointer to data stream
    stream_note_LO .dsb 6 ;stream_note_LO .rs 6        ;low 8 bits of period for the current note on a stream
    stream_note_HI .dsb 6 ;stream_note_HI .rs 6        ;high 3 bits of period for the current note on a stream
    stream_tempo .dsb 6          ;the value to add to our ticker total each frame
    stream_ticker_total .dsb 6   ;our running ticker total.
    stream_note_length_counter .dsb 6
    stream_note_length .dsb 6    ;note length count value
    stream_ve .dsb 6         ;current volume envelope
    stream_ve_index .dsb 6   ;current position within the volume envelope


    .ende

sound_init:
    LDA #$0F
    STA $4015   ;enable Square 1, Square 2, Triangle and Noise channels

    LDA #$00
    STA sound_disable_flag  ;clear disable flag

    lda #$FF
    sta sound_sq1_old
    sta sound_sq2_old

se_silence:
    lda #$30
    sta soft_apu_ports      ;set Square 1 volume to 0
    sta soft_apu_ports+4    ;set Square 2 volume to 0
    sta soft_apu_ports+12   ;set Noise volume to 0
    lda #$80
    sta soft_apu_ports+8     ;silence Triangle

    RTS

sound_disable:
    LDA #$00
    STA $4015   ;disable all channels
    LDA #$01
    STA sound_disable_flag  ;set disable flag
    RTS

;-------------------------------------
; load_sound will prepare the sound engine to play a song or sfx.
;   input:
;       A: song/sfx number to play
sound_load:
    STA sound_temp1         ;save song number
    ASL A                   ;multiply by 2.  We are indexing into a table of pointers (words)
    TAY
    LDA song_headers, Y     ;setup the pointer to our song header
    STA sound_ptr
    LDA song_headers+1, Y
    STA sound_ptr+1

    LDY #$00
    LDA (sound_ptr), Y      ;read the first byte: # streams
    STA sound_temp2         ;store in a temp variable.  We will use this as a loop counter
    INY
loop:
    LDA (sound_ptr), Y      ;stream number
    TAX                     ;stream number acts as our variable index
    INY

    LDA (sound_ptr), Y      ;status byte.  1= enable, 0=disable
    STA stream_status, X
    BEQ next_stream        ;if status byte is 0, stream disabled, so we are done
    INY

    LDA (sound_ptr), Y      ;channel number
    STA stream_channel, X
    INY

    LDA (sound_ptr), Y      ;initial duty and volume settings
    STA stream_vol_duty, X
    INY

    lda (sound_ptr), y      ;the stream's volume envelope
    sta stream_ve, x
    iny

    LDA (sound_ptr), Y      ;pointer to stream data.  Little endian, so low byte first
    STA stream_ptr_LO, X
    INY

    LDA (sound_ptr), Y
    STA stream_ptr_HI, X

    lda	#$ff
    sta	stream_ticker_total, x

    lda	#$01
    sta	stream_note_length_counter, x
    sta	stream_note_length, x

    lda	#$00
    sta	stream_ve_index, x
next_stream:
    INY

    LDA sound_temp1         ;song number
    STA stream_curr_sound, X

    DEC sound_temp2         ;our loop counter
    BNE loop
    RTS

;--------------------------
; sound_play_frame advances the sound engine by one frame
sound_play_frame:
    LDA sound_disable_flag
    BNE done   ;if sound engine is disabled, don't advance a frame

    ;; Silence all channels. se_set_apu will set volumen later for all
    ;; channels that are enabled. The purpose of this subroutine call is
    ;; to silence all channels that aren't used by any streams
    jsr	se_silence

    LDX #$00                ;our stream index.  start at MUSIC_SQ1 stream
frameloop:
    LDA stream_status, X    ;check bit 0 to see if stream is enabled
    AND #$01
    BEQ frame_next_stream        ;if disabled, skip to next stream

    lda stream_ticker_total, x
    clc
    adc stream_tempo, x
    sta stream_ticker_total, x
    bcc frame_next_stream    ;carry clear = no tick. if no tick, we are done with this stream

    dec stream_note_length_counter, x   ;else there is a tick. decrement the note length counter
    bne frame_next_stream    ;if counter is non-zero, our note isn't finished playing yet
    lda stream_note_length, x   ;else our note is finished. reload the note length counter
    sta stream_note_length_counter, x

    JSR se_fetch_byte       ;read from the stream and update RAM
    jsr se_set_temp_ports


frame_next_stream:
    INX
    CPX #$06                ;loop through all 6 streams.
    BNE frameloop

    JSR se_set_apu          ;write volume/duty, sweep, and note periods of current stream to the APU ports
done:
    RTS

;--------------------------
; se_fetch_byte reads one byte from a sound data stream and handles it
;   input:
;       X: stream number
se_fetch_byte:
    LDA stream_ptr_LO, X    ;copy stream pointer into a zero page pointer variable
    STA (sound_ptr)
    LDA stream_ptr_HI, X
    STA (sound_ptr)+1

    LDY #$00

fetch:
    LDA (sound_ptr), Y      ;read a byte using indirect mode
    BPL note               ;if <#$80, we have a note
    CMP #$A0                ;else if <#$A0 we have a note length
    BCC note_length
opcode:                    ;else we have an opcode
    ;nothing here yet
    JMP update_pointer
note_length:
    and #%01111111          ;chop off bit7
    sty sound_temp1         ;save Y because we are about to destroy it
    tay
    lda note_length_table, y    ;get the note length count value
    sta stream_note_length, x   ;save the note length in RAM so we can use it to refill the counter
    sta stream_note_length_counter, x   ;stick it in our note length counter
    ldy sound_temp1         ;restore Y
    iny                     ;set index to next byte in the stream
    jmp fetch              ;fetch another byte
note:
    ASL                     ;multiply by 2 because we are index into a table of words
    STY sound_temp1         ;save our Y register because we are about to destroy it
    TAY
    LDA note_table, y       ;pull low 8-bits of period and store it in RAM
    STA stream_note_LO, x
    LDA note_table+1, y     ;pull high 3-bits of period from our note table
    STA stream_note_HI, x
    LDY sound_temp1         ;restore the Y register

    lda #$00
    sta stream_ve_index, x  ;reset the volume envelope.

    ;check if it's a rest and modify the status flag appropriately
    jsr se_check_rest

 ;update our stream pointers to point to the next byte in the data stream
 update_pointer:
    INY                     ;set index to the next byte in the data stream
    TYA
    CLC
    ADC stream_ptr_LO, x    ;add Y to the LO pointer
    STA stream_ptr_LO, x
    BCC end
    INC stream_ptr_HI, x    ;if there was a carry, add 1 to the HI pointer.
end:
    RTS

;---------------------------CHECK REST---------------------------------------
se_check_rest:
    lda (sound_ptr), y  ;read the note byte again
    cmp #rest           ;is it a rest? (==$5E)
    bne @not_rest
    lda stream_status, x
    ora #%00000010      ;if so, set the rest bit in the status byte
    bne @store          ;this will always branch.  bne is cheaper than a jmp.
@not_rest:
    lda stream_status, x
    and #%11111101      ;clear the rest bit in the status byte
@store:
    sta stream_status, x
    rts
;---------------------------END CHECK REST---------------------------------------

;----------------------------SET TEMP PORTS------------------------------------------
se_set_temp_ports:
    lda stream_channel, x
    asl a
    asl a
    tay

    jsr se_set_stream_volume    ;let's stick all of our volume code into a new subroutine
                                ;less cluttered that way
    lda #$08
    sta soft_apu_ports+1, y     ;sweep

    lda stream_note_LO, x
    sta soft_apu_ports+2, y     ;period LO

    lda stream_note_HI, x
    sta soft_apu_ports+3, y     ;period HI

    rts
;---------------------------- END SET TEMP PORTS------------------------------------------

se_set_stream_volume:
    sty sound_temp1             ;save our index into soft_apu_ports (we are about to destroy y)

    lda stream_ve, x            ;which volume envelope?
    asl a                       ;multiply by 2 because we are indexing into a table of addresses (words)
    tay
    lda volume_envelopes, y     ;get the low byte of the address from the pointer table
    sta sound_ptr               ;put it into our pointer variable
    lda volume_envelopes+1, y   ;get the high byte of the address
    sta sound_ptr+1

@read_ve:
    ldy stream_ve_index, x      ;our current position within the volume envelope.
    lda (sound_ptr), y          ;grab the value.
    cmp #$FF
    bne @set_vol                ;if not FF, set the volume
    dec stream_ve_index, x      ;else if FF, go back one and read again
    jmp @read_ve                ;  FF essentially tells us to repeat the last
                                ;  volume value for the remainder of the note
@set_vol:
    sta sound_temp2             ;save our new volume value (about to destroy A)

    cpx #TRIANGLE
    bne @squares                ;if not triangle channel, go ahead
    lda sound_temp2
    bne @squares                ;else if volume not zero, go ahead (treat same as squares)
    lda #$80
    bmi @store_vol              ;else silence the channel with #$80

@squares:
    lda stream_vol_duty, x      ;get current vol/duty settings
    and #$F0                    ;zero out the old volume
    ora sound_temp2             ;OR our new volume in.

@store_vol:
    ldy sound_temp1             ;get our index into soft_apu_ports
    sta soft_apu_ports, y       ;store the volume in our temp port
    inc stream_ve_index, x      ;set our volume envelop index to the next position

@rest_check:
    ;check the rest flag. if set, overwrite volume with silence value
    lda stream_status, x
    and #%00000010
    beq @done                   ;if clear, no rest, so quit
    lda stream_channel, x
    cmp #TRIANGLE               ;if triangle, silence with #$80
    beq @tri                    ;else, silence with #$30
    lda #$30
    bne @store                  ;this always branches.  bne is cheaper than a jmp
@tri:
    lda #$80
@store:
    sta soft_apu_ports, y
@done:
    rts

;----------------------------SET APU------------------------------------------
se_set_apu:
@square1:
    lda soft_apu_ports+0
    sta $4000
    lda soft_apu_ports+1
    sta $4001
    lda soft_apu_ports+2
    sta $4002
    lda soft_apu_ports+3
    cmp sound_sq1_old       ;compare to last write
    beq @square2            ;don't write this frame if they were equal
    sta $4003
    sta sound_sq1_old       ;save the value we just wrote to $4003
@square2:
    lda soft_apu_ports+4
    sta $4004
    lda soft_apu_ports+5
    sta $4005
    lda soft_apu_ports+6
    sta $4006
    lda soft_apu_ports+7
    cmp sound_sq2_old
    beq @triangle
    sta $4007
    sta sound_sq2_old       ;save the value we just wrote to $4007
@triangle:
    lda soft_apu_ports+8
    sta $4008
    lda soft_apu_ports+10
    sta $400A
    lda soft_apu_ports+11
    sta $400B
@noise:
    lda soft_apu_ports+12
    sta $400C
    lda soft_apu_ports+14
    sta $400E
    lda soft_apu_ports+15
    sta $400F
    rts

;-----------------------------------------------------------------------------

NUM_SONGS = $02 ;if you add a new song, change this number.
                ;the main asm file checks this number in its song_up and song_down subroutines
                ;to determine when to wrap around.

song_headers:
    .dw song0_header
    .dw song1_header

    .include "note_table.i"
    .include "note_length_table.i"
    .include "volume_envelopes.i"
    .include "song0.i"
    .include "song1.i"
