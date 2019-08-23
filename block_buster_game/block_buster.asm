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

; bar verical size
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


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Default values for variables
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
BALL_X = 10
BALL_Y = 10
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
    move_bar_direction .dsb 1

    ball_x .dsb 1
    ball_y .dsb 1
    ball_vx .dsb 1
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
    STA     move_bar_direction

    LDA     #SCORE_LEFT
    STA     score_left
    LDA     #SCORE_RIGHT
    STA     score_right
    LDA     #GOAL_FLAG
    STA     goal_flag

    JMP     main_loop

NMI:

    ;NOTE: NMI code goes here
    
    JMP NMI

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
move_ball:
    LDA     ball_x                  ; load ball x into A
    CLC                             ; clean carry
    ADC     ball_vx                 ; sum it with ball_vx
    STA     ball_x                  ; save ball_x to variable
    LDA     ball_y                  ; load ball y into A
    CLC
    ADC     ball_vy                 ; sum it with ball_vy
    STA     ball_y                  ; save ball_y to variable
    RTS
; end mode_ball


players_move:
    ; TODO: implement bar movement, depends on input
    RTS
;end players_move


change_ball_vy:
    LDA     ball_vy                 ; load ball vy into A
    JSR     invert                  ; invert ball_vy
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
    BCC     CHECK_HIT_END           ; branch IF ball_y < DOWN_LIMIT 
    CMP     #UP_LIMIT               ; compare ball_y with UP_LIMIT
    BPL     CHECK_HIT_END           ; branch IF ball_y > UP_LIMIT
                                    ; ELSE (DOWN <= ball || ball <= UP)
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
    BCS     CHECK_GOAL_RIGHT        ; if ball_x > LEFT_LIMIT -> not goal     
                                    ; ELSE
    INC     score_right             ; increment score right
    LDA     #1       
    STA     goal_flag               ; store 1 in goal_flag
    JMP     wait
CHECK_GOAL_RIGHT:
    CLC
    ADC     #BALL_DIAMETER          ; add ball diameter to check on right side
    CMP     #RIGHT_LIMIT            ; compare ball_x with RIGHT_LIMIT
    BCC     CHECK_GOAL_END          ; if ball_x < RIGHT_LIMIT -> not goal
                                    ; ELSE
    INC     score_left              ; increment score left
    LDA     #2       
    STA     goal_flag               ; store 2 in goal_flag
    RTS
CHECK_GOAL_END:
    LDA     #0       
    STA     goal_flag               ; store 0 in goal_flag
    RTS
; end check_goal


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

; Updates the life count on screen.
update_life_count:


; Updates the score on screen.
update_score:

; Makes sound when ball hits a brick.
makes_sound_brick:

; Makes sound when ball hits the lava.
makes_sound_lava:

; Makes sound when the game ends.
makes_sound_game_over:

; Starts phase again, keeping the score. In other words, resets the bricks.
next_phase:

; Prints start message and waits for user input to start game.
game_start:

; Prints message at end of game and waits for user input to restart game.
game_over:

; Prints the bricks on screen.
print_bricks:

; Prints the ball on screen.
print_ball:

; Prints lava on screen.
print_lava:

; Prints the border on screen.
print_border:

; Reads the user input.
read_user_input:


infinite_loop:
    jmp infinite_loop

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

   .incbin "tiles.chr"
