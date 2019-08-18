;----------------------------------------------------------------
; constants
;----------------------------------------------------------------

PRG_COUNT = 1 ;1 = 16KB, 2 = 32KB
MIRRORING = %0001 ;%0000 = horizontal, %0001 = vertical, %1000 = four-screen

;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000

   ;NOTE: declare variables using the DSB and DSW directives, like this:

   ;MyVariable0 .dsb 1
   ;MyVariable1 .dsb 3

    slider_position .dsb 100

    ; 0 -> don't move
    ; 1 -> move left
    ; 2 -> move right
    move_slider .dsb 0

    ball_position_x .dsb 100
    ball_position_y .dsb 50
    ball_speed_x .dsb 3
    ball_speed_y .dsb 3

    score .dsb 0
    lives .dsb 3

    ; Each bit corresponds to one brick. If the bit is set the corresponding
    ; brick is in the screen
    ; least significant bit corresponds to brick 0
    bricks0 .dsb 255
    bricks1 .dsb 255
    bricks2 .dsb 255
    bricks3 .dsb 255
    bricks4 .dsb 255
    bricks5 .dsb 255
    bricks6 .dsb 255
    bricks7 .dsb 255
    

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

   .base $10000-(PRG_COUNT*$4000)

Reset:

   ;NOTE: initialization code goes here

NMI:

   ;NOTE: NMI code goes here

IRQ:

   ;NOTE: IRQ code goes here

; Change location of the ball based on horizontal and vertical speed.
move_ball:

; Change position of the bar depending on user input.
move_bar:

; Checks if the ball hits the bar.
check_hits_bar:

; Checks if the ball hits one of the bricks.
check_hits_brick:

; Checks if the ball hits the lava.
check_hits_lava:

; Checks if the call hits the walls.
check_hits_walls:

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

;----------------------------------------------------------------
; interrupt vectors
;----------------------------------------------------------------

   .org $fffa

   .dw NMI
   .dw Reset
   .dw IRQ

;----------------------------------------------------------------
; CHR-ROM bank
;----------------------------------------------------------------

   .incbin "tiles.chr"
