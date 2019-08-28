;----------------------------------------------------------------
; constants
;----------------------------------------------------------------

PRG_COUNT = 2 ;1 = 16KB, 2 = 32KB
MIRRORING = %0001 ;%0000 = horizontal, %0001 = vertical, %1000 = four-screen


;   Refer to this for the bar related constants
;
; DOWN                                          UP
;
;      position_y
;       -------------------------------------     bar_surface (relative to 0)
;      |     bar                             |
;      |                                     |
;~~~~~~ ------------------------------------- ~~~~~~  LEFT_LIMIT/RIGHT_LIMIT
;
;===================================================  end of screen (0 or 256)

; bar vertical size
BAR_SIZE = 8

; left bar surface (relative to 0)
LEFT_BAR_SURFACE = 20

; right bar surface (relative to 0)
RIGHT_BAR_SURFACE = 236

; How many pixels bar move if button is pressed
BAR_SPEED = 1

LEFT_LIMIT = 10
RIGHT_LIMIT = 246
UP_LIMIT = 76
DOWN_LIMIT = 223

BALL_DIAMETER = 8

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Default values for variables
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
BALL_X = 235
BALL_Y = 80
BALL_VX = 1
BALL_VY = 1

BAR_LEFT_Y = 200
BAR_RIGHT_Y = 95
MOVE_BAR_DIRECTION = 0

SCORE_LEFT = 0
SCORE_RIGHT = 0
GOAL_FLAG = 0

;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000    ;put variables starting at 0

   ;NOTE: declare variables using the.dsb and DSW directives, like this:

    ; bar left Y position
    bar_left_y .dsb 1
    ; bar right Y position
    bar_right_y .dsb 1

    ; 0 -> don't move
    ; 1 -> move up
    ; 2 -> move down
    move_p1_bar_direction .dsb 1
    move_p2_bar_direction .dsb 1

    ball_x .dsb 1
    ball_y .dsb 1
    ball_vx .dsb 2
    ball_vy .dsb 1

    score_left .dsb 1
    score_right .dsb 1
    goal_flag .dsb 1

    sleeping .dsb 1
    sound_ptr:    .dsb 2

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
; First 8k of PRG-ROM to SOUND
;----------------------------------------------------------------

   .base $10000-(PRG_COUNT*$4000)
   .include "sound_engine.asm"

;;;;;;;;;;;;;;;

   .org $C000

Reset:

    ; Initialize variables with default value

    lda     #SCORE_LEFT
    sta     score_left
    lda     #SCORE_RIGHT
    sta     score_right
    jsr     setup_game


; ------------------------- BACKGROUND ----------------------------------------

; -------------- LOAD PALETTES --------------------------------------
LoadPalettes:
    lda $2002             ; read PPU status to reset the high/low latch
    lda #$3F
    sta $2006             ; write the high byte of $3F00 address
    lda #$00
    sta $2006             ; write the low byte of $3F00 address

    ldx #$00              ; use x as "iterator" - start at 0
LoadPalettesLoop:
    lda palette, x        ; load from (palette + the value in x)
    sta $2007             ; write to PPU
    inx                   ; increment "iterator"
    cpx #$20              ; Compare X to hex $20, loading 32 colors = 2 palettes
    bne LoadPalettesLoop
;---------------------------------------------------------------------

; ----------- LOAD SPRITES -------------------------------------------
LoadSprites:
    ldx #$00              ; start at 0
LoadSpritesLoop:
    lda sprites, x        ; load from (sprites +  x)
    sta $0200, x          ; store into RAM address ($0200 + x)
    inx
    cpx #$14              ; loads 5 sprites
    bne LoadSpritesLoop
;----------------------------------------------------------------------

; ------------ LOAD BACKGROUND ----------------------------------------
LoadBackground:
    lda $2002             ; read PPU status to reset the high/low latch
    lda #$20
    sta $2006             ; write the high byte of $2000 address
    lda #$00
    sta $2006             ; write the low byte of $2000 address

; ------- TOP WALL -------
    ldx #$00
LoopBGTopWall:            ; Loads wall on top of the screen
    lda background_hwall, x
    sta $2007
    inx
    cpx #$20              ; 1 row
    bne LoopBGTopWall

; -------- HEADER --------
    ldx #$00              ; Loads header on screen ("player 1" and "player 2")
LoopBGHeader:
    lda background_header, x
    sta $2007
    inx
    cpx #$40              ; 2 rows
    bne LoopBGHeader

; ----- SCORE AREA -------
    ldy #$00              ; Loads score area on screen (where score sprites will go)
OutsideLoopBGScoreArea:   ; Used two loops because register x isn't big enough.
    ldx #$00
LoadBGScoreArea:
    lda background_vwall, x
    sta $2007
    inx
    cpx #$20              ; 1 row
    bne LoadBGScoreArea
    iny
    cpy #$4               ; 4 times
    bne OutsideLoopBGScoreArea

; ----- DIVISION WALL ----
    ldx #$00              ; Loads a line of horizontal wall on screen.
LoopBGDivision:
    lda background_hwall, x
    sta $2007
    inx
    cpx #$20              ; 1 row
    bne LoopBGDivision

; ----- GAME/LAVA ---------
    ldy #$00              ; Loads game background with lava on the sides.
OutsideLoopBGLava:        ; Uses two loops because x isn't big enough.
    ldx #$00
LoadBGLava:
    lda background_lava, x
    sta $2007
    inx
    cpx #$40              ; 2 rows
    bne LoadBGLava
    iny
    cpy #$09              ; 9 times (9x2 = 18 rows)
    bne OutsideLoopBGLava

; ----- BOTTOM WALL -------
    ldx #$00              ; Loads bottom wall on screen
LoopBGBottomWall:
    lda background_hwall, x
    sta $2007
    inx
    cpx #$20              ; 1 row
    bne LoopBGBottomWall
;------------------------------------------------------------------------

; -------------- LOAD ATTRIBUTES ----------------------------------------
LoadAttribute:
    lda $2002             ; read PPU status to reset the high/low latch
    lda #$23
    sta $2006             ; write the high byte of $23C0 address
    lda #$C0
    sta $2006             ; write the low byte of $23C0 address

    ldx #$00
LoadAttributeLoop:
    lda attribute, x      ; load from (attribute + the value in x)
    sta $2007             ; write to PPU
    inx
    cpx #$10              ; Compare X to hex $10 - two lines of attributes (16 bytes)
    bne LoadAttributeLoop
;----------------------------------------------------------------------------

    lda #%10000000   ; enable NMI, both sprites and background from Pattern Table 0.
    sta $2000
    lda #%00011110   ; enable sprites, enable background, no clipping on left side
    sta $2001

; ------- END OF BACKGROUND --------------------------------------------------

; ------------------------------ SOUND ----------------------------------------
; ---------------------- ENABLE SOUNDS ----------------------------
    jsr sound_init

    lda #$00
    jsr sound_load
; -----------------------------------------------------------------

; ------------------------------ END OF SOUND ---------------------------------

    jmp     main_loop

NMI:

    ;NOTE: NMI code goes here
    sei

    pha         ; back up registers (important)
    txa
    pha
    tya
    pha


    lda #$00
    sta $2003       ; set the low byte (00) of the RAM address
    lda #$02
    sta $4014       ; set the high byte (02) of the RAM address, start the transfer

    jsr UpdateSprites ; Update sprites on screen

;----------- Comment the following line to disable the song ----------------
    jsr sound_play_frame    ;run our sound engine after all drawing code is done.
                            ;this ensures our sound engine gets run once per frame.

    lda     #0
    sta     sleeping

    pla            ; restore regs and exit
    tay
    pla
    tax
    pla
    cli
    rti


IRQ:
    rti



; -----------------------------------------------------------------------------
; begin foooooo



; Utilities

; Register Y -> 1 if value in A register is negative, else to Y -> 0
is_negative:
	cmp     #$7F
	bpl     IS_NEGATIVE_NEG_LABEL
	ldy     #0
	rts
IS_NEGATIVE_NEG_LABEL:
	ldy     #1
	rts
; end is_negative


; Invert value in A register. Equivalent to A = -A
invert:
	eor     #$FF
	clc
	adc     #1
	rts
;end invert


; Set A to the module of the value in A. A = |A|
module:
	jsr     is_negative
  cpy     #0
	bne     MODULE_NEG_LABEL
	rts
MODULE_NEG_LABEL:
	jsr     invert
	rts
;end module


setup_game:

    ; Initialize variables with default value
    lda     #BALL_X
    sta     ball_x
    lda     #BALL_Y
    sta     ball_y
    lda     #BALL_VX
    sta     ball_vx
    lda     #BALL_VY
    sta     ball_vy

    lda     #BAR_LEFT_Y
    sta     bar_left_y
    lda     #BAR_RIGHT_Y
    sta     bar_right_y
    lda     #MOVE_BAR_DIRECTION
    sta     move_p1_bar_direction
    sta     move_p2_bar_direction

    lda     #GOAL_FLAG
    sta     goal_flag
    rts
; end setup_game


.org   $C200
main_loop:
    jsr     check_hits_something
    jsr     players_move
    jsr     move_ball
    jsr     wait
    jmp     main_loop
; end main_loop

; Change location of the ball based on horizontal and vertical speed.
.org $C300
move_ball:
    lda     ball_x                  ; load ball x into A
    clc                             ; clean carry
    adc     ball_vx                 ; sum it with ball_vx
    cmp     #LEFT_LIMIT             ; check horizontal limits
    bcs     MOVE_CHECK_RIGHT        ; if ball_x >= LEFT_LIMIT
                                    ; ELSE limit ball_x
    lda     #LEFT_LIMIT             ; ball_x = LEFT_LIMIT
    sta     ball_x                  ; save ball_x to variable
    jsr     right_scored            ; touch left limit -> right scored
    jmp     MOVE_BALL_Y             ; no need to test RIGHT

MOVE_CHECK_RIGHT:
    clc
    adc     #BALL_DIAMETER          ; add ball diameter to compare RIGHT
    cmp     #RIGHT_LIMIT
    bcc     END_MOVE_BALL_X         ; if ball_x < RIGHT_LIMIT
                                    ; ELSE limit ball_x
    jsr     left_scored             ; touch right -> left scored
    lda     #RIGHT_LIMIT            ; ball_x = RIGHT_LIMIT (subtract 8 below)
END_MOVE_BALL_X:
    sec
    sbc     #BALL_DIAMETER          ; subtract diameter after tests
    sta     ball_x

MOVE_BALL_Y:
    lda     ball_y                  ; load ball y into A
    clc
    adc     ball_vy                 ; sum it with ball_vy
    cmp     #UP_LIMIT               ; check vertical limits
    beq     MOVE_BALL_L1
    bcs     MOVE_CHECK_DOWN         ; if ball_y > UP_LIMIT

MOVE_BALL_L1:                       ; ELSE limit ball_y
    lda     #UP_LIMIT               ; ball_y = UP_LIMIT
    sta     ball_y                  ; save ball_y to variable
    jsr     change_ball_vy
    jmp     END_MOVE_BALL           ; no need to test DOWN

MOVE_CHECK_DOWN:
    clc
    adc     #BALL_DIAMETER          ; add ball diameter to compare DOWN
    cmp     #DOWN_LIMIT
    bcc     END_MOVE_BALL_Y         ; if ball_y < DOWN_LIMIT
                                    ; ELSE limit ball_y and change ball_vy
    jsr     change_ball_vy          ; invert ball_vy
    lda     #DOWN_LIMIT             ; ball_y = DOWN_LIMIT (subtract 8 below)

END_MOVE_BALL_Y:
    sec
    sbc     #BALL_DIAMETER          ; subtract diameter after tests
    sta     ball_y

END_MOVE_BALL:
    rts
; end mode_ball





change_ball_vy:
    lda     ball_vy                 ; load ball vy into A
    jsr     invert                  ; invert ball_vy
    sta     ball_vy
    rts
;end ball_vy

change_ball_vx:
    lda     ball_vx                 ; load ball vx into A
    jsr     invert                  ; invert ball_vx
    rts
;end ball_vx


; Checks if the ball hits the bar.
check_hits_something:
    ; this is now done in move_ball so to not allow ball to pass walls
    jsr     check_hit_bars          ; check if hit bars (this order is not
                                    ; intuitive but may make sense in math)
    jsr     check_hit_mid_bar       ; check if ball hit middle bar
    rts
;end check_hits_something


; Checks if the ball hits the walls.
check_hits_walls:
    lda     ball_y                  ; load ball_y into A
    cmp     #DOWN_LIMIT             ; compare with DOWN_LIMIT
    bcs     HIT_WALL                ; branch IF ball_y >= DOWN_LIMIT
    cmp     #UP_LIMIT               ; compare ball_y with UP_LIMIT
    beq     HIT_WALL
    bcs     CHECK_HIT_END           ; branch IF ball_y > UP_LIMIT
                                    ; ELSE (DOWN <= ball || ball <= UP)
HIT_WALL:
    lda     ball_vy                 ; load ball_vy into A
    jsr     invert                  ; invert ball_vy
    sta     ball_vy                 ; save ball_vy
CHECK_HIT_END:
    rts

; end check_hits_walls

; Checks if a goal was scored
right_scored:
    inc     score_right             ; increment score right
    lda     score_right             ; limit scores to 9
    cmp     #10
    bne     R_SCORED_L1
    lda     #0
    sta     score_right
    sta     score_left
R_SCORED_L1:
    lda     #1
    sta     goal_flag               ; store 1 in goal_flag
    rts
; end right_scored

left_scored:
    inc     score_left              ; increment score left
    lda     score_left              ; limit scores to 9
    cmp     #10
    bne     L_SCORED_L1
    lda     #0
    sta     score_right
    sta     score_left
L_SCORED_L1:
    lda     #2
    sta     goal_flag               ; store 2 in goal_flag
    rts
; end left_scored

;reset_score_right:
;    sta     score_right
;    rts


;       BALL HITS BAR LOGIC
;
; At this point we know that LEFT_LIMIT < ball_x < RIGHT_LIMIT because we
; passed check_goal and no one scored. We need only to check if:
;
;
;       ball_x <= left_bar_surface
;   AND
;       left_bar_y - bar_size_y <= ball_y <= left_bar_y + 8
; OR
;       ball_x >= right_bar_surface
;   AND
;       right_bar_y - bar_size_y <= ball_y <= right_bar_y + 8

; check if ball_y fits in left/right bar vertical limits
; expects in register A the bar_y which is being tested
; returns A = 1 if hit bar, A = 0 otherwise
test_bar_y_limits:
    sec
    sbc     #BAR_SIZE               ; subtract BAR_SIZE
    cmp     ball_y
    beq     Y_LIM_L1
    bcs     TEST_VERT_BAR_FALSE     ; bar_y-bar_size > ball_y -> ball is over

Y_LIM_L1:
    clc
    adc     #BAR_SIZE               ; sum BAR_SIZE
    clc
    adc     #BALL_DIAMETER          ; sum BALL_DIAMETER
    cmp     ball_y
    bcc     TEST_VERT_BAR_FALSE     ; bar_y + 8 < ball_y -> ball is under

    lda     #1
    rts

TEST_VERT_BAR_FALSE:
    lda     #0
    rts

.org    $C400
check_hit_bars:
    lda     ball_x                  ; load ball x into A
    cmp     #LEFT_BAR_SURFACE
    beq     TEST_LEFT_BAR_Y         ; test vertical pos if ball_x <= left_bar_x
    bcs     TEST_RIGHT_BAR
TEST_LEFT_BAR_Y:
    lda     bar_left_y              ; load left_bar_y into A and test Y limits
    jsr     test_bar_y_limits
    cmp     #0
    beq     NO_HIT                  ; no need to test right bar at this point
    lda     #0                      ; load 0 to A and call ball_hit_bar
    jsr     ball_hit_bar
    rts

TEST_RIGHT_BAR:
    lda     ball_x                  ; load ball_x into A
    cmp     #RIGHT_BAR_SURFACE
    bcc     NO_HIT                  ; if ball_x < right_bar_surface -> no hit

    lda     bar_right_y             ; load right_bar_y into A and test Y limits
    jsr     test_bar_y_limits
    cmp     #0
    beq     NO_HIT
    lda     #1                      ; load 1 to A and call ball_hit_bar
    jsr     ball_hit_bar
    rts

NO_HIT:
    rts
; end check_hit_bars


; do something when ball hits bar. Expects in A: 0 if hit left bar, 1 if right
ball_hit_bar:
    ; For now, invert both ball_vx and ball_vy
    lda     ball_vy
    jsr     invert
    sta     ball_vy
    lda     ball_vx
    jsr     invert
    sta     ball_vx

    rts


check_hit_mid_bar:
    ; TODO: implement
    rts
;end check_hit_mid_bar


wait:
    inc     sleeping
SLEEP:
    lda     sleeping
    bne     SLEEP
    rts
; end wait

goal_scored:
    jsr     setup_game
    ; TODO: setup screen and start match
    ;jmp     wait
    rts
; end foooooo
;-----------------------------------------------------------------------------

; Makes sound when ball hits a brick.
makes_sound_brick:

; Makes sound when ball hits the lava.
makes_sound_lava:

; Makes sound when the game ends.
makes_sound_game_over:

; Prints start message and waits for user input to start game.
game_start:

; Prints message at end of game and waits for user input to restart game.
game_over:

;------------------------------------------------------------------------------
;------------------- MOVE PLAYER BARS (PADDLES) -------------------------------

players_move:
    jsr MOVE_PLAYER_1
    jsr MOVE_PLAYER_2
    rts

; ----------------- PLAYER 1 ------------------
MOVE_PLAYER_1:
    jsr read_p1_input               ; Read input from player 1

    lda move_p1_bar_direction
    cmp #$00                        ; Not moving
    beq END_MOVE_P1_BAR
    cmp #$01                        ; Moving up
    beq MOVE_P1_BAR_UP
    cmp #$02                        ; Moving down
    beq MOVE_P1_BAR_DOWN

; ---- PLAYER 1 - MOVE UP ----
MOVE_P1_BAR_UP:
    lda bar_left_y
    sec
    sbc #BAR_SPEED
    cmp #UP_LIMIT
    bcc END_MOVE_P1_BAR             ; If position is less the up limit, do nothing
    beq END_MOVE_P1_BAR
    sta bar_left_y                  ; Updates bar position
    jmp END_MOVE_P1_BAR

; ---- PLAYER 1 - MOVE DOWN ---
MOVE_P1_BAR_DOWN:       ; NOTE: when using instr clc before ADC, doesnt work.
    lda bar_left_y
    adc #BAR_SIZE
    adc #BAR_SPEED
    cmp #DOWN_LIMIT
    bcs END_MOVE_P1_BAR
    sbc #BAR_SIZE
    sta bar_left_y
    jmp END_MOVE_P1_BAR

END_MOVE_P1_BAR:
    rts
;----------------------------------------------

; ----------------- PLAYER 2 ------------------
MOVE_PLAYER_2:
    jsr read_p2_input               ; Read input from player 2

    lda move_p2_bar_direction
    cmp #$00                        ; Not moving
    beq END_MOVE_P2_BAR
    cmp #$01                        ; Moving up
    beq MOVE_P2_BAR_UP
    cmp #$02                        ; Moving down
    beq MOVE_P2_BAR_DOWN

; ---- PLAYER 2 - MOVE UP ----
MOVE_P2_BAR_UP:
    lda bar_right_y
    sec
    sbc #BAR_SPEED
    cmp #UP_LIMIT
    bcc END_MOVE_P2_BAR             ; If position is less then up limit, do nothing
    beq END_MOVE_P2_BAR
    sta bar_right_y                  ; Updates bar position
    jmp END_MOVE_P2_BAR

; ---- PLAYER 2 - MOVE DOWN ---
MOVE_P2_BAR_DOWN:       ; NOTE: when using instr clc before ADC, doesnt work.
    lda bar_right_y
    adc #BAR_SIZE
    adc #BAR_SPEED
    cmp #DOWN_LIMIT
    bcs END_MOVE_P2_BAR
    sbc #BAR_SIZE
    sta bar_right_y
    jmp END_MOVE_P2_BAR

END_MOVE_P2_BAR:
    rts
;----------------------------------------------

;------------------------ END OF MOVE PLAYER BARS ------------------------------
;-------------------------------------------------------------------------------


;--------------------------- READ INPUT FROM PLAYERS ---------------------------

; ------------- PLAYER 1 -----------------
read_p1_input:
    ; LatchController P1
    lda #$01
    sta $4016
    lda #$00
    sta $4016

    ; Set P1 bar to not move (Could not validate. Possible issue)
    lda #$00
    sta move_p1_bar_direction

    ; Ignore A, B, Select and Start buttons
    lda $4016
    lda $4016
    lda $4016
    lda $4016

;------ READ PLAYER 1 UP BUTTOM ----
READ_UP_P1:
    lda $4016
    and #%00000001
    beq READ_UP_END_P1

    ; Set p1 direction up
    lda #$01
    sta move_p1_bar_direction
READ_UP_END_P1:

;----- READ PLAYER 1 DOWN BUTTOM ---
READ_DOWN_P1:
    lda $4016
    and #%00000001
    beq READ_DOWN_END_P1

    ; Set p1 direction down
    lda #$02
    sta move_p1_bar_direction
READ_DOWN_END_P1:
    rts
;--------- END READ INPUT P1 -------------

; ------------- PLAYER 2 -----------------
read_p2_input:
    ; LatchController P2
    lda #$01
    sta $4017
    lda #$00
    sta $4017

    ; Set P2 bar to not move (Could not validate. Possible issue)
    lda #$00
    sta move_p2_bar_direction

    ; Ignore A, B, Select and Start buttons
    lda $4017
    lda $4017
    lda $4017
    lda $4017

;------ READ PLAYER 2 UP BUTTOM ----
READ_UP_P2:
    lda $4017
    and #%00000001
    beq READ_UP_END_P2

    ; Set p2 direction up
    lda #$01
    sta move_p2_bar_direction
READ_UP_END_P2:

;----- READ PLAYER 2 DOWN BUTTOM ---
READ_DOWN_P2:
    lda $4017
    and #%00000001
    beq READ_DOWN_END_P2

    ; Set p2 direction down
    lda #$02
    sta move_p2_bar_direction
READ_DOWN_END_P2:
    rts
;--------- END READ INPUT P2 -------------

; ---------------------------- END OF READ INPUT ------------------------------
;------------------------------------------------------------------------------


;------------------------- UPDATE SPRITES ON SCREEN ---------------------------

UpdateSprites:      ; Changes sprites on screen. Ball moves, score is updated.
    lda ball_y        ; Update ball's position (x,y).
    sta $0200
    lda ball_x
    sta $0203

    lda score_left    ; Writes player 1's score on screen.
    adc #$23          ; Sprite with number zero.
    sta $020D

    lda score_right   ; Writes player 2's score on screen.
    adc #$23          ; Sprite with number zero.
    sta $0211

    lda bar_left_y    ; Updates position on player 1's paddle.
    sta $0204

    lda bar_right_y   ; Updates position on player 2' paddle.
    sta $0208

    rts
; ------------------------- END UPDATE SPRITES ---------------------------------
;-------------------------------------------------------------------------------

infinite_loop:
    jmp infinite_loop


;---------------------------- BACKGROUND SETUP ---------------------------------
; Mapping reference guide:
; P .. R-> 19 .. 1E
; Sky -> 40
; Numbers Mapping:
; 0 .. 9 -> 23 -> 2C
; Wins! -> 30,..,34

    .org $E000
palette:
    ;   lava              wall              letters           unused
    .db $0F,$16,$28,$22,  $14,$16,$28,$22,  $29,$29,$29,$29,  $29,$29,$29,$29   ;;background palette
    ;   ball              unused            unused            unused
    .db $0F,$16,$28,$22,  $29,$29,$29,$29,  $29,$29,$29,$29,  $29,$29,$29,$29   ;;sprites palette

sprites:
       ;vert tile attr horiz
    .db $90, $16, $00, $80   ;bola
    .db $90, $18, $00, $0A   ;bar player 1
    .db $90, $18, $00, $F0   ;bar player 2
scores:
    .db $30, $23, $00, $30   ;score player 1
    .db $30, $23, $00, $D0   ;score player 2


background_hwall:          ; Horizontal wall row
    .db $13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13
    .db $13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13

background_header:        ; Writes "player 1" and "player 2" on header
    .db $14,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40
    .db $40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$14

    .db $14,$40,$40,$19,$1A,$1B,$1C,$1D,$1E,$1F,$24,$40,$40,$40,$40,$40
    .db $40,$40,$40,$40,$40,$19,$1A,$1B,$1C,$1D,$1E,$1F,$25,$40,$40,$14

background_vwall:         ; Background with simple wall on the sides

    .db $14,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40
    .db $40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$14

background_lava:          ; Background with lava on the sides (2 types of lava)
    .db $10,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40
    .db $40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$20

    .db $11,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40
    .db $40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$40,$21

attribute:
    .db %10010101, %10100101, %10100101, %10100101, %10100101, %10100101, %10100101, %01100101
    .db %01010101, %01010101, %01010101, %01010101, %01010101, %01010101, %01010101, %01010101

; END BACKGROUND SETUP --------------------------------------------------------


;----------------------------------------------------------------
; interrupt vect.dsb
;----------------------------------------------------------------

   .org $fffa

   .dw NMI
   .dw Reset
   .dw IRQ

;----------------------------------------------------------------
; CHR-ROM bank
;----------------------------------------------------------------

   .incbin "sprites.chr"
