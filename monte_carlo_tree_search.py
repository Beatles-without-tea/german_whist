from german_whist import Play


new_game = Play(players=1)
new_game.deal()
new_game.play_first_half()
new_game.play_second_half()