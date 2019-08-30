;; Silence song. Disables all streams

song0_header:
  .db $06           ;6 streams

  .db MUSIC_SQ1     ;which stream
  .db $00           ;status byte (stream disabled)

  .db MUSIC_SQ2     ;which stream
  .db $00           ;status byte (stream disabled)

  .db MUSIC_TRI     ;which stream
  .db $00           ;status byte (stream disabled)

  .db MUSIC_NOI     ;which stream
  .db $00           ;disabled.

  .db SFX_1         ;which stream
  .db $00           ;disabled

  .db SFX_2         ;which stream
  .db $00           ;disabled
