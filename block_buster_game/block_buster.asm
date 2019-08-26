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

    LDA     #SCORE_LEFT
    STA     score_left
    LDA     #SCORE_RIGHT
    STA     score_right
    JSR     setup_game

; BACKGROUND -- STILL WORKING ON IT, PLEASE DONT TOUCH :)----------------------

LoadPalettes:
    LDA $2002             ; read PPU status to reset the high/low latch
    LDA #$3F
    STA $2006             ; write the high byte of $3F00 address
    LDA #$00
    STA $2006             ; write the low byte of $3F00 address
    LDX #$00              ; start out at 0
LoadPalettesLoop:
    LDA palette, x        ; load data from address (palette + the value in x)
                            ; 1st time through loop it will load palette+0
                            ; 2nd time through loop it will load palette+1
                            ; 3rd time through loop it will load palette+2
                            ; etc
    STA $2007             ; write to PPU
    INX                   ; X = X + 1
    CPX #$20              ; Compare X to hex $10, decimal 16 - copying 16 bytes = 4 sprites
    BNE LoadPalettesLoop  ; Branch to LoadPalettesLoop if compare was Not Equal to zero
                          ; if compare was equal to 32, keep going down


LoadSprites:
    LDX #$00              ; start at 0
LoadSpritesLoop:
    LDA sprites, x        ; load data from address (sprites +  x)
    STA $0200, x          ; store into RAM address ($0200 + x)
    INX                   ; X = X + 1
    CPX #$14              ; Compare X to hex $10, decimal 16
    BNE LoadSpritesLoop   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
                          ; if compare was equal to 16, keep going down


LoadBackground:
    LDA $2002             ; read PPU status to reset the high/low latch
    LDA #$20
    STA $2006             ; write the high byte of $2000 address
    LDA #$00
    STA $2006             ; write the low byte of $2000 address



    LDX #$00
LoadBackgroundLoop1:
    LDA background_hwall, x
    STA $2007
    INX
    CPX #$20
    BNE LoadBackgroundLoop1


    LDX #$00              ; Header
LoadBackgroundLoop2:
    LDA background_header, x
    STA $2007
    INX
    CPX #$40
    BNE LoadBackgroundLoop2

    LDY #$00              ; score area
ExternalLoop6:
    LDX #$00
LoadBackgroundLoop6:
    LDA background_vwall, x
    STA $2007
    INX
    CPX #$20
    BNE LoadBackgroundLoop6
    INY
    CPY #$4
    BNE ExternalLoop6

    LDX #$00              ; Dividing wall
LoadBackgroundLoop3:
    LDA background_hwall, x
    STA $2007
    INX
    CPX #$20
    BNE LoadBackgroundLoop3

    LDY #$00              ; Game wall
ExternalLoop4:
    LDX #$00
LoadBackgroundLoop4:
    LDA background_lava, x
    STA $2007
    INX
    CPX #$40
    BNE LoadBackgroundLoop4
    INY
    CPY #$09
    BNE ExternalLoop4

    LDX #$00              ; Lower wall
LoadBackgroundLoop5:
    LDA background_hwall, x
    STA $2007
    INX
    CPX #$20
    BNE LoadBackgroundLoop5


LoadAttribute:
    LDA $2002             ; read PPU status to reset the high/low latch
    LDA #$23
    STA $2006             ; write the high byte of $23C0 address
    LDA #$C0
    STA $2006             ; write the low byte of $23C0 address

    LDX #$00              ; start out at 0
LoadAttributeLoop:
    LDA attribute, x      ; load data from address (attribute + the value in x)
    STA $2007             ; write to PPU
    INX                   ; X = X + 1
    CPX #$10              ; Compare X to hex $08, decimal 8 - copying 8 bytes
    BNE LoadAttributeLoop  ; Branch to LoadAttributeLoop if compare was Not Equal to zero
                          ; if compare was equal to 128, keep going down


    LDA #%10000000   ; enable NMI, sprites from Pattern Table 0, background from Pattern Table 1
    STA $2000

    LDA #%00011110   ; enable sprites, enable background, no clipping on left side
    STA $2001

; END OF BACKGROUND -----------------------------------------------------------

    JMP     main_loop

NMI:

    ;NOTE: NMI code goes here

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


setup_game:

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

    LDA     #GOAL_FLAG
    STA     goal_flag
    RTS
; end setup_game


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
    ; this is now done in move_ball so to not allow ball to pass walls
    ;JSR     check_hits_walls        ; check if ball hit up or down walls

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
    JMP     goal_scored
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
    JMP     goal_scored
    
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


;       BALL HITS BAR LOGIC
;
; At this point we now that LEFT_LIMIT < ball_x < RIGHT_LIMIT because we
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
    CLC
    SBC     #BAR_SIZE               ; subtract BAR_SIZE
    CMP     ball_y
    BCC     TEST_VERT_BAR_FALSE     ; bar_y-bar_size < ball_y -> ball is over
    
    CLC
    ADC     #BAR_SIZE               ; sum BAR_SIZE
    CLC
    ADC     #BALL_DIAMETER          ; sum BALL_DIAMETER
    CMP     ball_y
    BEQ     TEST_VERT_BAR_TRUE
    BCS     TEST_VERT_BAR_FALSE     ; bar_y + 8 > ball_y -> ball is under

TEST_VERT_BAR_TRUE
    LDA     #1
    RTS

TEST_VERT_BAR_FALSE:
    LDA     #0
    RTS


check_hit_bars:
    LDA     ball_x                  ; load ball x into A
    CMP     #LEFT_BAR_SURFACE
    BEQ     TEST_LEFT_BAR_Y         ; test vertical pos if ball_x <= left_bar_x
    BCS     TEST_RIGHT_BAR
TEST_LEFT_BAR_Y:
    LDA     left_bar_y              ; load left_bar_y into A and test Y limits
    JSR     test_bar_y_limits
    CMP     #0
    BEQ     NO_HIT                  ; no need to test right bar at this point
    LDA     #0                      ; load 0 to A and call ball_hit_bar
    JSR     ball_hit_bar                 
    RTS

TEST_RIGHT_BAR:
    LDA     ball_x                  ; load ball_x into A
    CMP     #RIGHT_BAR_SURFACE
    BCC     NO_HIT                  ; if ball_x < right_bar_surface -> no hit

    LDA     right_bar_y             ; load right_bar_y into A and test Y limits
    JSR     test_bar_y_limits
    CMP     #0
    BEQ     NO_HIT
    LDA     #1                      ; load 1 to A and call ball_hit_bar
    JSR     ball_hit_bar                 
    RTS

NO_HIT:
    RTS
; end check_hit_bars


; do something when ball hits bar. Expects in A: 0 if hit left bar, 1 if right
ball_hit_bar:
    ; TODO: implement
    ; For now, invert both ball_vx and ball_vy
    LDA     ball_vy
    JSR     invert
    STA     ball_vy
    LDA     ball_vx
    JSR     invert
    STA     ball_vx
    RTS


check_hit_mid_bar:
    ; TODO: implement
    RTS
;end check_hit_mid_bar


wait:
    JMP     wait

goal_scored:
    JSR     setup_game
    ; TODO: setup screen and start match
    JMP     main_loop

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
    ;   lava              wall               letters
    .db $0F,$16,$28,$22,  $14,$16,$28,$22,  $29,$29,$29,$29,  $29,$29,$29,$29   ;;background palette
    .db $0F,$16,$28,$22,  $14,$16,$28,$22,  $29,$29,$29,$29,  $29,$29,$29,$29   ;;sprites palette

sprites:
       ;vert tile attr horiz
    .db $90, $17, $00, $80   ;bola
    .db $90, $18, $00, $0A   ;paddle 1
    .db $90, $18, $00, $F0   ;paddle 2
scores:
    .db $30, $1A, $00, $30   ;sprite 3
    .db $30, $1A, $00, $D0   ;sprite 3


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
