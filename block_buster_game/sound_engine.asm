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

    sound_frame_counter dsb 1


    ;reserve 6 bytes, one for each stream
    stream_curr_sound .dsb 6 ;stream_curr_sound .rs 6     ;current song/sfx loaded
    stream_status .dsb 6 ;stream_status .rs 6         ;status byte.   bit0: (1: stream enabled; 0: stream disabled)
    stream_channel .dsb 6 ;stream_channel .rs 6        ;what channel is this stream playing on?
    stream_vol_duty .dsb 6 ;stream_vol_duty .rs 6       ;stream volume/duty settings
    stream_ptr_LO .dsb 6 ;stream_ptr_LO .rs 6         ;low byte of pointer to data stream
    stream_ptr_HI .dsb 6 ;stream_ptr_HI .rs 6         ;high byte of pointer to data stream
    stream_note_LO .dsb 6 ;stream_note_LO .rs 6        ;low 8 bits of period for the current note on a stream
    stream_note_HI .dsb 6 ;stream_note_HI .rs 6        ;high 3 bits of period for the current note on a stream

    .ende

sound_init:
    LDA #$0F
    STA $4015   ;enable Square 1, Square 2, Triangle and Noise channels

    LDA #$30
    STA $4000   ;set Square 1 volume to 0
    STA $4004   ;set Square 2 volume to 0
    STA $400C   ;set Noise volume to 0
    LDA #$80
    STA $4008   ;silence Triangle

    LDA #$00
    STA sound_disable_flag  ;clear disable flag

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

    LDA (sound_ptr), Y      ;pointer to stream data.  Little endian, so low byte first
    STA stream_ptr_LO, X
    INY

    LDA (sound_ptr), Y
    STA stream_ptr_HI, X
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

    INC sound_frame_counter
    LDA sound_frame_counter
    CMP #$08    ;***change this compare value to make the notes play faster or slower***
    BNE done   ;only take action once every 8 frames.

    LDX #$00                ;our stream index.  start at MUSIC_SQ1 stream
frameloop:
    LDA stream_status, X    ;check bit 0 to see if stream is enabled
    AND #$01
    BEQ frame_next_stream        ;if disabled, skip to next stream

    JSR se_fetch_byte       ;read from the stream and update RAM
    JSR se_set_apu          ;write volume/duty, sweep, and note periods of current stream to the APU ports

frame_next_stream:
    INX
    CPX #$06                ;loop through all 6 streams.
    BNE frameloop

    LDA #$00
    STA sound_frame_counter ;reset frame counter so we can start counting to 8 again.
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
    LDA (sound_ptr), Y      ;read a byte using indirect mode
    BPL note               ;if <#$80, we have a note
    CMP #$A0                ;else if <#$A0 we have a note length
    BCC note_length
opcode:                    ;else we have an opcode
    ;nothing here yet
    JMP update_pointer
note_length:
    ;nothing here yet
    JMP update_pointer
note:
    ASL                     ;multiply by 2 because we are index into a table of words
    STY sound_temp1         ;save our Y register because we are about to destroy it
    TAY
    LDA note_table, y       ;pull low 8-bits of period and store it in RAM
    STA stream_note_LO, x
    LDA note_table+1, y     ;pull high 3-bits of period from our note table
    STA stream_note_HI, x
    LDY sound_temp1         ;restore the Y register

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

se_set_apu:
    LDA stream_channel, X   ;which channel does this stream write to?
    ASL A
    ASL A                   ;multiply by 4 so Y will index into the right set of APU ports (see below)
    TAY
    LDA stream_vol_duty, X
    STA $4000, Y
    LDA stream_note_LO, X
    STA $4002, Y
    LDA stream_note_HI, X
    STA $4003, Y

    LDA stream_channel, X
    CMP #TRIANGLE
    BCS set_apu_end:        ;if Triangle or Noise, skip this part
    LDA #$08        ;else, set negate flag in sweep unit to allow low notes on Squares
    STA $4001, Y
set_apu_end:
    RTS

NUM_SONGS = $01 ;if you add a new song, change this number.
                ;the main asm file checks this number in its song_up and song_down subroutines
                ;to determine when to wrap around.

song_headers:
    .dw song0_header

    .include "note_table.i"
    .include "song0.i"
