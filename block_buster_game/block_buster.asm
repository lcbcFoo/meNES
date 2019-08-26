;----------------------------------------------------------------
; constants
;----------------------------------------------------------------

PRG_COUNT = 1 ;1 = 16KB, 2 = 32KB
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
BAR_SIZE = 20

; left bar surface (relative to 0)
LEFT_BAR_SURFACE = 20

; right bar surface (relative to 0)
RIGHT_BAR_SURFACE = 236

; How many pixels bar move if button is pressed
BAR_SPEED = 1

LEFT_LIMIT = 10
RIGHT_LIMIT = 246
UP_LIMIT = 50
DOWN_LIMIT = 200

BALL_DIAMETER = 8
SCORE_LIMIT = 10

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Default values for variables
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
BALL_X = 11
BALL_Y = 80
BALL_VX = 1
BALL_VY = 1

BAR_LEFT_Y = 100
BAR_RIGHT_Y = 100
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
; program bank(s)
;----------------------------------------------------------------

   .org $C000

Reset:

    ; Initialize variables with default value
    LDA     #BALL_X
    STA     ball_x
    LDA     #BALL_Y
    STA     ball_y
    LDA     #BALL_VX
    STA     ball_vx
    LDA     #BALL_VY
    STA     ball_vy

    LDA     #BAR_LEFT_Y
    STA     bar_left_y
    LDA     #BAR_RIGHT_Y
    STA     bar_right_y
    LDA     #MOVE_BAR_DIRECTION
    STA     move_p1_bar_direction
    STA     move_p2_bar_direction

    LDA     #SCORE_LEFT
    STA     score_left
    LDA     #SCORE_RIGHT
    STA     score_right
    LDA     #GOAL_FLAG
    STA     goal_flag


; ------------------------- BACKGROUND ----------------------------------------

; -------------- LOAD PALETTES --------------------------------------
LoadPalettes:
    LDA $2002             ; read PPU status to reset the high/low latch
    LDA #$3F
    STA $2006             ; write the high byte of $3F00 address
    LDA #$00
    STA $2006             ; write the low byte of $3F00 address

    LDX #$00              ; use x as "iterator" - start at 0
LoadPalettesLoop:
    LDA palette, x        ; load from (palette + the value in x)
    STA $2007             ; write to PPU
    INX                   ; increment "iterator"
    CPX #$20              ; Compare X to hex $20, loading 32 colors = 2 palettes
    BNE LoadPalettesLoop
;---------------------------------------------------------------------

; ----------- LOAD SPRITES -------------------------------------------
LoadSprites:
    LDX #$00              ; start at 0
LoadSpritesLoop:
    LDA sprites, x        ; load from (sprites +  x)
    STA $0200, x          ; store into RAM address ($0200 + x)
    INX
    CPX #$14              ; loads 5 sprites
    BNE LoadSpritesLoop
;----------------------------------------------------------------------

; ------------ LOAD BACKGROUND ----------------------------------------
LoadBackground:
    LDA $2002             ; read PPU status to reset the high/low latch
    LDA #$20
    STA $2006             ; write the high byte of $2000 address
    LDA #$00
    STA $2006             ; write the low byte of $2000 address

; ------- TOP WALL -------
    LDX #$00
LoopBGTopWall:            ; Loads wall on top of the screen
    LDA background_hwall, x
    STA $2007
    INX
    CPX #$20              ; 1 row
    BNE LoopBGTopWall

; -------- HEADER --------
    LDX #$00              ; Loads header on screen ("player 1" and "player 2")
LoopBGHeader:
    LDA background_header, x
    STA $2007
    INX
    CPX #$40              ; 2 rows
    BNE LoopBGHeader

; ----- SCORE AREA -------
    LDY #$00              ; Loads score area on screen (where score sprites will go)
OutsideLoopBGScoreArea:   ; Used two loops because register x isn't big enough.
    LDX #$00
LoadBGScoreArea:
    LDA background_vwall, x
    STA $2007
    INX
    CPX #$20              ; 1 row
    BNE LoadBGScoreArea
    INY
    CPY #$4               ; 4 times
    BNE OutsideLoopBGScoreArea

; ----- DIVISION WALL ----
    LDX #$00              ; Loads a line of horizontal wall on screen.
LoopBGDivision:
    LDA background_hwall, x
    STA $2007
    INX
    CPX #$20              ; 1 row
    BNE LoopBGDivision

; ----- GAME/LAVA ---------
    LDY #$00              ; Loads game background with lava on the sides.
OutsideLoopBGLava:        ; Uses two loops because x isn't big enough.
    LDX #$00
LoadBGLava:
    LDA background_lava, x
    STA $2007
    INX
    CPX #$40              ; 2 rows
    BNE LoadBGLava
    INY
    CPY #$09              ; 9 times (9x2 = 18 rows)
    BNE OutsideLoopBGLava

; ----- BOTTOM WALL -------
    LDX #$00              ; Loads bottom wall on screen
LoopBGBottomWall:
    LDA background_hwall, x
    STA $2007
    INX
    CPX #$20              ; 1 row
    BNE LoopBGBottomWall
;------------------------------------------------------------------------

; -------------- LOAD ATTRIBUTES ----------------------------------------
LoadAttribute:
    LDA $2002             ; read PPU status to reset the high/low latch
    LDA #$23
    STA $2006             ; write the high byte of $23C0 address
    LDA #$C0
    STA $2006             ; write the low byte of $23C0 address

    LDX #$00
LoadAttributeLoop:
    LDA attribute, x      ; load from (attribute + the value in x)
    STA $2007             ; write to PPU
    INX
    CPX #$10              ; Compare X to hex $10 - two lines of attributes (16 bytes)
    BNE LoadAttributeLoop
;----------------------------------------------------------------------------

    LDA #%10000000   ; enable NMI, both sprites and background from Pattern Table 0.
    STA $2000
    LDA #%00011110   ; enable sprites, enable background, no clipping on left side
    STA $2001

; ------- END OF BACKGROUND --------------------------------------------------
;-----------------------------------------------------------------------------

    JMP     main_loop

NMI:

    LDA #$00
    STA $2003       ; set the low byte (00) of the RAM address
    LDA #$02
    STA $4014       ; set the high byte (02) of the RAM address, start the transfer

    JSR UpdateSprites ; Update sprites on screen

    RTI             ; return from interrupt

IRQ:
    JMP Reset
   ;NOTE: IRQ code goes here



; -----------------------------------------------------------------------------
; begin foooooo



; Utilities

; Register Y -> 1 if value in A register is negative, else to Y -> 0
is_negative:
	CMP     #$7F
	BPL     IS_NEGATIVE_NEG_LABEL
	LDY     #0
	RTS
IS_NEGATIVE_NEG_LABEL:
	LDY     #1
	RTS
; end is_negative


; Invert value in A register. Equivalent to A = -A
invert:
	EOR     #$FF
	CLC
	ADC     #1
	RTS
;end invert


; Set A to the module of the value in A. A = |A|
module:
	JSR     is_negative
    CPY     #0
	BNE     MODULE_NEG_LABEL
	RTS
MODULE_NEG_LABEL:
	JSR     invert
	RTS
;end module

.org   $C200
main_loop:
    JSR     check_hits_something
    JSR     players_move
    JSR     move_ball
    JSR     main_loop
; end main_loop

; Change location of the ball based on horizontal and vertical speed.
.org $C300
move_ball:
    LDA     ball_x                  ; load ball x into A
    CLC                             ; clean carry
    ADC     ball_vx                 ; sum it with ball_vx
    CMP     #LEFT_LIMIT             ; check horizontal limits
    BCS     MOVE_CHECK_RIGHT        ; if ball_x >= LEFT_LIMIT
                                    ; ELSE limit ball_x
    LDA     #LEFT_LIMIT             ; ball_x = LEFT_LIMIT
    STA     ball_x                  ; save ball_x to variable
    JMP     MOVE_BALL_Y             ; no need to test RIGHT

MOVE_CHECK_RIGHT:
    CLC
    ADC     #BALL_DIAMETER          ; add ball diameter to compare RIGHT
    CMP     #RIGHT_LIMIT
    BCC     END_MOVE_BALL_X         ; if ball_x < RIGHT_LIMIT
                                    ; ELSE limit ball_x
    LDA     #RIGHT_LIMIT            ; ball_x = RIGHT_LIMIT (subtract 8 below)
END_MOVE_BALL_X:
    SEC
    SBC     #BALL_DIAMETER          ; subtract diameter after tests
    STA     ball_x

MOVE_BALL_Y:
    LDA     ball_y                  ; load ball y into A
    CLC
    ADC     ball_vy                 ; sum it with ball_vy
    CMP     #UP_LIMIT               ; check vertical limits
    BCS     MOVE_CHECK_DOWN         ; if ball_y >= UP_LIMIT
                                    ; ELSE limit ball_y
    LDA     #UP_LIMIT               ; ball_y = UP_LIMIT
    STA     ball_y                  ; save ball_y to variable
    JMP     END_MOVE_BALL           ; no need to test DOWN

MOVE_CHECK_DOWN:
    CLC
    ADC     #BALL_DIAMETER          ; add ball diameter to compare DOWN
    CMP     #DOWN_LIMIT
    BCC     END_MOVE_BALL_Y         ; if ball_y < DOWN_LIMIT
                                    ; ELSE limit ball_y and change ball_vy
    JSR     change_ball_vy          ; invert ball_vy
    LDA     #DOWN_LIMIT             ; ball_y = DOWN_LIMIT (subtract 8 below)

END_MOVE_BALL_Y:
    SEC
    SBC     #BALL_DIAMETER          ; subtract diameter after tests
    STA     ball_y

END_MOVE_BALL:
    RTS
; end mode_ball


players_move:
    ; TODO: implement bar movement, depends on input
    RTS
;end players_move


change_ball_vy:
    LDA     ball_vy                 ; load ball vy into A
    JSR     invert                  ; invert ball_vy
    STA     ball_vy
    RTS
;end ball_vy

change_ball_vx:
    LDA     ball_vx                 ; load ball vx into A
    JSR     invert                  ; invert ball_vx
    RTS
;end ball_vx


; Checks if the ball hits the bar.
check_hits_something:
    JSR     check_hits_walls        ; check if ball hit up or down walls
    JSR     check_goal              ; check if a goal happened
    JSR     check_hit_bars          ; check if hit bars (this order is not
                                    ; intuitive but may make sense in math)
    JSR     check_hit_mid_bar       ; check if ball hit middle bar
    RTS
;end check_hits_something


; Checks if the ball hits the walls.
check_hits_walls:
    LDA     ball_y                  ; load ball_y into A
    CMP     #DOWN_LIMIT             ; compare with DOWN_LIMIT
    BCS     HIT_WALL                ; branch IF ball_y >= DOWN_LIMIT
    CMP     #UP_LIMIT               ; compare ball_y with UP_LIMIT
    BEQ     HIT_WALL
    BCS     CHECK_HIT_END           ; branch IF ball_y > UP_LIMIT
                                    ; ELSE (DOWN <= ball || ball <= UP)
HIT_WALL:
    LDA     ball_vy                 ; load ball_vy into A
    JSR     invert                  ; invert ball_vy
    STA     ball_vy                 ; save ball_vy
CHECK_HIT_END:
    RTS

; end check_hits_walls

; Checks if a goal was scored
check_goal:
    LDA     ball_x                  ; load ball_x into A
    CMP     #LEFT_LIMIT             ; compare with left of screen
    BEQ     RIGHT_GOAL
    BCS     CHECK_GOAL_RIGHT        ; if ball_x > LEFT_LIMIT -> not goal
                                    ; ELSE
RIGHT_GOAL:
    INC     score_right             ; increment score right
    LDA     #1
    STA     goal_flag               ; store 1 in goal_flag
    ;JMP     wait
    RTS
CHECK_GOAL_RIGHT:
    CLC
    ADC     #BALL_DIAMETER          ; add ball diameter to check on right side
    CMP     #RIGHT_LIMIT            ; compare ball_x with RIGHT_LIMIT
    BCC     CHECK_GOAL_END          ; if ball_x < RIGHT_LIMIT -> not goal
                                    ; ELSE
    INC     score_left              ; increment score left
    ;LDA     score_left             ; TODO: set max number for score
    ;CMP     #SCORE_LIMIT
    ;BEQ     reset_score_left
    LDA     #2
    STA     goal_flag               ; store 2 in goal_flag
    RTS
CHECK_GOAL_END:
    LDA     #0
    STA     goal_flag               ; store 0 in goal_flag
    RTS
; end check_goal

reset_score_left:
    STA     score_left
    RTS

reset_score_right:
    STA     score_right
    RTS


check_hit_bars:
    ; TODO: implement
    RTS

check_hit_mid_bar:
    ; TODO: implement
    RTS
;end check_hit_mid_bar


wait:
    JMP     wait

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


; Reads the p1 input.
read_p1_input:
; LatchController P1
    LDA #$01
    STA $4016
    LDA #$00
    STA $4016

; Set P1 bar to not move (Could not validate. Possible issue)
    LDA #$00
    STA move_p1_bar_direction

; Ignore A, B, Select and Start buttons
    LDA $4016
    LDA $4016
    LDA $4016
    LDA $4016

; Read Player 1 Up Button
READ_UP_P1:
    LDA $4016
    AND #%00000001
    BEQ READ_UP_END_P1

; Set p1 direction up
    LDA #$01
    STA move_p1_bar_direction
READ_UP_END_P1:

; Read Player 1 Down Button
READ_DOWN_P1:
    LDA $4016
    AND #%00000001
    BEQ READ_DOWN_END_P1

; Set p1 direction down
    LDA #$02
    STA move_p1_bar_direction
READ_DOWN_END_P1:

RTS
;end read_p1_input

; Reads the p2 input.
read_p2_input:
; LatchController P2
    LDA #$01
    STA $4017
    LDA #$00
    STA $4017

; Set P2 bar to not move (Could not validate. Possible issue)
    LDA #$00
    STA move_p2_bar_direction

; Ignore A, B, Select and Start buttons
    LDA $4017
    LDA $4017
    LDA $4017
    LDA $4017

; Read Player 2 Up Button
READ_UP_P2:
    LDA $4017
    AND #%00000001
    BEQ READ_UP_END_P2

; Set p2 direction up
    LDA #$01
    STA move_p2_bar_direction
READ_UP_END_P2:

; Read Player 2 Down Button
READ_DOWN_P2:
    LDA $4017
    AND #%00000001
    BEQ READ_DOWN_END_P2

; Set p2 direction down
    LDA #$02
    STA move_p2_bar_direction
READ_DOWN_END_P2:

RTS
;end read_p2_input

UpdateSprites:      ; Changes sprites on screen. Ball moves, score is updated.
  LDA ball_y        ; Update ball's position (x,y).
  STA $0200
  LDA ball_x
  STA $0203

  LDA score_left    ; Writes player 1's score on screen.
  ADC #$1A          ; Sprite with number zero.
  STA $020D

  LDA score_right   ; Writes player 2's score on screen.
  ADC #$1A          ; Sprite with number zero.
  STA $0211

  ; TODO: update paddle sprites

  RTS

infinite_loop:
    jmp infinite_loop


; BACKGROUND SETUP ------------------------------------------------------------
; Mapping reference guide:
; P .. R-> 23 .. 28
; Sky -> 2C
; Numbers Mapping:
; 0,6 -> 19 .. 1F
; 7,8,9 -> 29, 2A, 2B

    .org $E000
palette:
    ;   lava              wall              letters           unused
    .db $0F,$16,$28,$22,  $14,$16,$28,$22,  $29,$29,$29,$29,  $29,$29,$29,$29   ;;background palette
    ;   ball              unused            unused            unused
    .db $0F,$16,$28,$22,  $29,$29,$29,$29,  $29,$29,$29,$29,  $29,$29,$29,$29   ;;sprites palette

sprites:
       ;vert tile attr horiz
    .db $90, $17, $00, $80   ;bola
    .db $90, $18, $00, $0A   ;paddle 1
    .db $90, $18, $00, $F0   ;paddle 2
scores:
    .db $30, $1A, $00, $30   ;score player 1
    .db $30, $1A, $00, $D0   ;score player 2


background_hwall:          ; Horizontal wall row
    .db $13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13
    .db $13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13,$13

background_header:        ; Writes "player 1" and "player 2" on header
    .db $14,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C
    .db $2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$14

    .db $14,$2C,$2C,$23,$24,$25,$26,$27,$28,$2C,$1A,$2C,$2C,$2C,$2C,$2C
    .db $2C,$2C,$2C,$2C,$2C,$23,$24,$25,$26,$27,$28,$2C,$1B,$2C,$2C,$14

background_vwall:         ; Background with simple wall on the sides

    .db $14,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C
    .db $2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$14

background_lava:          ; Background with lava on the sides (2 types of lava)
    .db $10,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C
    .db $2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$20

    .db $11,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C
    .db $2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$2C,$21

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
