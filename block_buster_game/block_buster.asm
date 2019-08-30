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
LEFT_BAR_SURFACE = 19

; right bar surface (relative to 0)
RIGHT_BAR_SURFACE = 237

; How many pixels bar move if button is pressed
BAR_SPEED = 2

LEFT_LIMIT = 10
RIGHT_LIMIT = 246
UP_LIMIT = 76
DOWN_LIMIT = 223

BALL_DIAMETER = 8

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Default values for variables
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
BALL_X = 140
BALL_Y = 93
BALL_VX = 1
BALL_VY = 1
MAX_POSITIVE_SPEED = 6
MAX_NEGATIVE_SPEED = $f0

BAR_LEFT_Y = 140
BAR_RIGHT_Y = 140
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
    start_button_p1 .dsb 1
    start_button_p2 .dsb 1

    ball_x .dsb 1
    ball_y .dsb 1
    ball_vx .dsb 1
    ball_vy .dsb 1

    dummy .dsb 1
    score_left .dsb 1
    score_right .dsb 1
    goal_flag .dsb 1
    last_start .dsb 1

    sleeping .dsb 1
    hit_bar_flag .dsb 1


    ;SOUND POINTERS
    sound_ptr:    .dsb 2
    sound_ptr2:   .dsb 2
    ;jmp_ptr:      .dsb 2 Possible problem. Check later

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

    ;sei			; Disable IRQs
    ;cld			; Disable decimal mode
    ldx	#$ff		; Set up stack
    txs			;  .
    inx			; Now X = 0

    ;; First wait for vblank to make sure PPU is ready
vblankwait1:
    bit	$2002
    bpl	vblankwait1

clear_memory:
  	lda	#$00
  	sta	$0000, x
  	sta	$0100, x
  	sta	$0300, x
  	sta	$0400, x
  	sta	$0500, x
  	sta	$0600, x
  	sta	$0700, x
  	lda	#$fe
  	sta	$0200, x	; Move all sprites off screen
  	inx
  	bne	clear_memory

	;; Second wait for vblank, PPU is ready after this
vblankwait2:
  	bit	$2002
  	bpl	vblankwait2

clear_nametables:
  	lda	$2002		; Read PPU status to reset the high/low latch
  	lda	#$20		; Write the high byte of $2000
  	sta	$2006		;  .
  	lda	#$00		; Write the low byte of $2000
  	sta	$2006		;  .
  	ldx	#$08		; Prepare to fill 8 pages ($800 bytes)
  	ldy	#$00		;  x/y is 16-bit counter, high byte in x
  	lda	#$00		; Fill with tile $00 (a transparent box)
  				; Also sets attribute tables to $00
@loop:
  	sta	$2007
  	dey
  	bne	@loop
  	dex
  	bne	@loop


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

LoadSpritesGame:
    ldx #$00              ; start at 0
LoadSpritesLoop:
    lda sprites, x        ; load from (sprites +  x)
    sta $0200, x          ; store into RAM address ($0200 + x)
    inx
    cpx #$14              ; loads 5 sprites
    bne LoadSpritesLoop

LoadPress:
    ldx #$00
LoadPressLoop:
    lda sprites_press, x
    sta $0214, x
    inx
    cpx #$14
    bne LoadPressLoop

LoadStart:
    ldx #$00
LoadStartLoop:
    lda sprites_start, x
    sta $0228, x
    inx
    cpx #$14
    bne LoadStartLoop
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

;------------------------------- WAIT START------------------------------------
WaitForStart:
      jsr read_p1_input
      lda start_button_p1
      cmp #$01
      beq WaitForStartEnd
      jsr read_p2_input
      lda start_button_p2
      cmp #$01
      bne WaitForStart
WaitForStartEnd:

;------------- ERASE SPRITES FOR START OF THE GAME -----------------------------

EraseOtherSprites:
    ldx #$00
EraseSpritesLoop:
    lda blank_sprite
    sta $0214, x
    inx
    cpx #$28
    bne EraseSpritesLoop
;------------------------------------------------------------------------------

; ------------------------------ SOUND ----------------------------------------
; ---------------------- ENABLE SOUNDS ----------------------------
    jsr sound_init

    lda #$01
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
	bcs     IS_NEGATIVE_NEG_LABEL
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

    lda     #0
    sta     hit_bar_flag

    ; make ball start to left and next time to right
    lda     last_start
    beq     CHANGE_START
    lda     #BALL_VX
    jsr     invert
    sta     ball_vx
    lda     #0
    sta     last_start
    jmp     SETUP_Y
CHANGE_START:
    lda     #BALL_VX
    sta     ball_vx
    lda     #1
    sta     last_start

SETUP_Y:
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


main_loop:
    jsr     avoid_multiple_hits
    jsr     move_ball
    jsr     check_game_status
    jsr     check_hits_something
    jsr     players_move
    jsr     wait
    jmp     main_loop
; end main_loop


check_game_status:
    lda     goal_flag
    beq     END_STATUS
    jsr     setup_game
    lda     #0
    sta     goal_flag
    rts

END_STATUS:
    rts


; Change location of the ball based on horizontal and vertical speed.
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
    jsr     makes_sound_brick
    lda     ball_vy                 ; load ball vy into A
    jsr     invert                  ; invert ball_vy
    sta     ball_vy
    rts
;end ball_vy

change_ball_vx:
    lda     ball_vx                 ; load ball vx into A
    jsr     invert                  ; invert ball_vx
    sta     ball_vx
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
    jsr     makes_sound_game_over
    lda     #0
    sta     score_right
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
    jsr     makes_sound_game_over
    lda     #0
    sta     score_left
L_SCORED_L1:
    lda     #2
    sta     goal_flag               ; store 2 in goal_flag
    rts
; end left_scored


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

check_hit_bars:
    lda     ball_x                  ; load ball x into A
    cmp     #LEFT_BAR_SURFACE
    beq     TEST_LEFT_BAR_Y         ; test vertical pos if ball_x <= left_bar_x
    bcs     TEST_RIGHT_BAR
TEST_LEFT_BAR_Y:
    lda     bar_left_y              ; load bar_left_y into A and test Y limits
    jsr     test_bar_y_limits
    cmp     #0
    beq     NO_HIT                  ; no need to test right bar at this point

    lda     bar_left_y              ; load bar_left_y to A and call ball_hit_bar
    jsr     ball_hit_bar
    rts

TEST_RIGHT_BAR:
    lda     ball_x                  ; load ball_x into A
    clc
    adc     #BALL_DIAMETER
    cmp     #RIGHT_BAR_SURFACE
    bcc     NO_HIT                  ; if ball_x < right_bar_surface -> no hit

    lda     bar_right_y             ; load bar_right_y into A and test Y limits
    jsr     test_bar_y_limits
    cmp     #0
    beq     NO_HIT

    lda     bar_right_y             ; load bar_right_y to A and call ball_hit_bar
    jsr     ball_hit_bar
    rts

NO_HIT:
    rts
; end check_hit_bars


avoid_multiple_hits:
    pha                             ; save A to stack
    lda     hit_bar_flag
    beq     END_AVOID
    sec
    sbc     #1
    sta     hit_bar_flag
    pla
    rts

END_AVOID:
    pla                             ; restore A from stack
    rts


; do something when ball hits bar. Expects in A: 0 if hit left bar, 1 if right
ball_hit_bar:
    pha                             ; save A to stack
    jsr     makes_sound_brick
    lda     hit_bar_flag
    beq     CAN_HIT_BAR
    pla
    rts

CAN_HIT_BAR:
    lda     #7
    sta     hit_bar_flag
    pla

    clc
    adc     #BALL_DIAMETER
    sec
    sbc     ball_y
    cmp     #5
    bcs     L1_HIT_BAR
    ; ball hit first quarter of the bar, ball_vy = |ball_vy| + 1
    lda     ball_vy
    jsr     module
    clc
    adc     #1
    cmp     #MAX_POSITIVE_SPEED
    bcc     L0_HIT_BAR
    lda     #(MAX_POSITIVE_SPEED-1)

L0_HIT_BAR:
    sta     ball_vy
    jmp     INVERT_VX

L1_HIT_BAR:
    cmp     #10
    bcs     L2_HIT_BAR
    ; ball hit second quarter of the bar, ball_vy = |y|
    lda     ball_vy
    jsr     module
    sta     ball_vy
    jmp     RAISE_SPEED_VX

L2_HIT_BAR:
    cmp     #15
    bcs     L3_HIT_BAR
    ; ball hit third quarter of the bar, ball_vy = -|y|
    lda     ball_vy
    jsr     module
    jsr     invert
    sta     ball_vy
    jmp     RAISE_SPEED_VX

L3_HIT_BAR:
    ; ball hit last quarter of the bar, ball_vy = -(|y|+1)
    lda     ball_vy
    jsr     module
    clc
    adc     #1
    cmp     #MAX_POSITIVE_SPEED
    bcc     L4_HIT_BAR
    lda     #(MAX_POSITIVE_SPEED-1)
L4_HIT_BAR
    jsr     invert
    sta     ball_vy

RAISE_SPEED_VX
    ; raise speed_x
    lda     ball_vx
    jsr     is_negative
    cpy     #0
	bne     HIT_BAR_INC_NEG_VX      ; if ball_vx is positive -> increment 1
    clc
    adc     #1
    cmp     #MAX_POSITIVE_SPEED
    bcc     RAISE_SPEED_VX_1
    lda     #MAX_POSITIVE_SPEED
RAISE_SPEED_VX_1:
    sta     ball_vx
    jmp     INVERT_VX

HIT_BAR_INC_NEG_VX:                 ; if ball_vx is negative -> subtract 1
    sec
    sbc     #1
    cmp     #MAX_NEGATIVE_SPEED
    bcs     RAISE_SPEED_VX_2
    lda     #MAX_NEGATIVE_SPEED
RAISE_SPEED_VX_2:
    sta     ball_vx

INVERT_VX:
    lda     ball_vx
    jsr     invert
    sta     ball_vx
    rts
; end ball_hit_bar


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

; end foooooo
;-----------------------------------------------------------------------------

; Makes sound when ball hits a brick.
makes_sound_brick:
    lda #$02
    jsr sound_load
    rts

; Makes sound when ball hits the lava.
makes_sound_lava:

; Makes sound when the game ends.
makes_sound_game_over:
    lda #$00
    jsr sound_load
    lda #$03
    jsr sound_load
    rts

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
    sta start_button_p1

    ; Ignore A, B and Select buttons
    lda $4016
    lda $4016
    lda $4016

;------ READ PLAYER 1 START BUTTOM ----
READ_START_P1:
    lda $4016
    and #%00000001
    beq READ_START_END_P1

    ; Set p1 direction up
    lda #$01
    sta start_button_p1
READ_START_END_P1:

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
    sta start_button_p2

    ; Ignore A, B, Select and Start buttons
    lda $4017
    lda $4017
    lda $4017

;------ READ PLAYER 2 START BUTTOM ----
READ_START_P2:
    lda $4017
    and #%00000001
    beq READ_START_END_P2

    ; Set p1 direction up
    lda #$01
    sta start_button_p2
READ_START_END_P2:

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
    clc
    adc #$23          ; Sprite with number zero.
    sta $020D

    lda score_right   ; Writes player 2's score on screen.
    clc
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
    .db $90, $37, $00, $0A   ;bar player 1
    .db $90, $36, $00, $F0   ;bar player 2
scores:
    .db $30, $23, $00, $30   ;score player 1
    .db $30, $23, $00, $D0   ;score player 2

sprites_press:
    .db $90, $19, $00, $70   ;P
    .db $90, $1E, $00, $78   ;R
    .db $90, $1D, $00, $80   ;E
    .db $90, $33, $00, $88   ;S
    .db $90, $33, $00, $90   ;S

sprites_start:
    .db $98, $33, $00, $70   ;S
    .db $98, $35, $00, $78   ;T
    .db $98, $1B, $00, $80   ;A
    .db $98, $1E, $00, $88   ;R
    .db $98, $35, $00, $90   ;T

blank_sprite:
    .db $00, $00, $00, $00   ;Blank piece of background


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
