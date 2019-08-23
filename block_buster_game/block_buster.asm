;----------------------------------------------------------------
; constants
;----------------------------------------------------------------

PRG_COUNT = 1 ;1 = 16KB, 2 = 32KB
MIRRORING = %0001 ;%0000 = horizontal, %0001 = vertical, %1000 = four-screen

; bar horizontal size
BAR_SIZE = 20

;   Refer to this for the following constants
;
;       -------------------------------------         bar_surface
;      |     bar                             |
;      |                                     |
;~~~~~~ ------------------------------------- ~~~~~~  lava_surface
;
;===================================================  end of screen (0)

; bar surface level (where the ball is supposed to hit)
BAR_SURFACE = 20
; Lava y level. If the ball goes under this point -> game over
LAVA_SURFACE = 11

LEFT_LIMIT = 10
RIGHT_LIMIT = 246
UP_LIMIT = 180

; Default values
BALL_X = 10
BALL_Y = 10
BALL_VX = 1
BALL_VY = 1

BAR_X = 100
MOVE_BAR_SELECT = 0

SCORE = 0
RECORD = 0
LIVES = 3

HITS_LAVA = 0
HITS_BAR = 0

BRICKS_HEIGHT = 10
BRICKS_WIDTH = 30

FIRST_BRICK_Y = 120

BRICKS0 = 10
BRICKS1 = 11
BRICKS2 = 12
BRICKS3 = 13
BRICKS4 = 14
BRICKS5 = 15
BRICKS6 = 16
BRICKS7 = 17

;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000    ;put variables starting at 0

   ;NOTE: declare variables using the.dsb and DSW directives, like this:

   ;MyVariable0 .dsb 1
   ;MyVariable1 .dsb 3

    ; bar X position
    bar_x .dsb 1

    ; 0 -> don't move
    ; 1 -> move left
    ; 2 -> move right
    move_bar_select .dsb 1

    ball_x .dsb 1
    ball_y .dsb 1
    ball_vx .dsb 1
    ball_vy .dsb 1

    score .dsb 1
    record .dsb 1
    lives .dsb 1

    ; Flag used by check_hits_lava. If set to one -> ball hits lava
    hits_lava .dsb 1

    ; Flag used by check_hits_bar. If set to one -> ball hits bar
    hits_bar .dsb 1

    ; Each bit corresponds to one brick. If the bit is set the corresponding
    ; brick is in the screen
    ; least significant bit corresponds to brick 0
    bricks .dsb 8
    

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

    LDA     #BAR_X
    STA     bar_x
    LDA     #MOVE_BAR_SELECT
    STA     move_bar_select

    LDA     #SCORE
    STA     score
    LDA     #RECORD
    STA     record
    LDA     #LIVES
    STA     lives

    LDA     #HITS_LAVA
    STA     hits_lava
    LDA     #HITS_BAR
    STA     hits_bar

    LDX     #1
    LDA     #BRICKS0
    STA     bricks,X
    INX
    LDA     #BRICKS1
    STA     bricks,X
    INX
    LDA     #BRICKS2
    STA     bricks,X
    INX
    LDA     #BRICKS3
    STA     bricks,X
    INX
    LDA     #BRICKS4
    STA     bricks,X
    INX
    LDA     #BRICKS5
    STA     bricks,X
    INX
    LDA     #BRICKS6
    STA     bricks,X
    INX
    LDA     #BRICKS7
    STA     bricks,X
    
    
    JMP check_hits_lava

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
	CMP #$7F
	BPL IS_NEGATIVE_NEG_LABEL
	LDY #0
	RTS
IS_NEGATIVE_NEG_LABEL:
	LDY #1
	RTS
; end is_negative


; Invert value in A register. Equivalent to A = -A
invert:
	EOR #$FF
	CLC
	ADC #1
	RTS
;end invert


; Set A to the module of the value in A. A = |A|
module:
	PHA
	JSR is_negative
	BNE MODULE_NEG_LABEL
	PLA
	RTS
MODULE_NEG_LABEL:
	PLA
	JSR invert
	RTS
;end module



; Change location of the ball based on horizontal and vertical speed.
move_ball:
    CLC                             ; clean carry
    LDA     ball_x                  ; load ball x into A
    ADC     ball_vx                 ; sum it with ball_vx
    STA     ball_x                  ; save ball_x to variable
    CLC
    LDA     ball_y                  ; load ball y into A
    ADC     ball_vy                 ; sum it with ball_vy
    STA     ball_y                  ; save ball_y to variable
    RTS
; end mode_ball


; Change position of the bar depending on user input.
move_bar:

; end move_bar


reflect_y:
    LDA     ball_vy                 ; load ball vy into A
    SEC     
    SBC     ball_vy                 ; subtract it 2 times, the result will be
    SEC
    SBC     ball_vy                 ; -ball_vy
    RTS


; Checks if the ball hits the bar.
check_hits_something:
    LDA     ball_y                  ; load ball y into A
    CMP     #BAR_SURFACE            ; compare with bar surface level
    BMI     hits_bar_label1         ; if result < 0 (is at same level or under
                                    ; bar_surface) goto hits_bar_label1
    CMP     #UP_LIMIT               ; compare with up limit
    BPL     
    RTS                         


hits_bar_label1:
    JSR     check_hits_lava         ; check if ball hit lava

    ; TODO

;end check_hits_bar


; Checks if the ball hits one of the bricks.
check_hits_brick:

;end check_hits_brick


; Checks if the ball hits the lava.
check_hits_lava:
    LDA     ball_y                  ; load ball y into A
    CMP     #LAVA_SURFACE           ; compare with lava level
    BMI     hits_lava_check_label   ; if result is < 0 goto check_label
    RTS                             ; else just return)
hits_lava_check_label:
    JMP     game_over


; Checks if the call hits the walls.
check_hits_walls:
    LDA     ball_y                  

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
