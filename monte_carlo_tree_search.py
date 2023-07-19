from german_whist import Play


new_game = Play(players=1)
new_game.deal()
for _ in range(13):
    new_game.play_first_half_round()
for _ in range(13):
    new_game.play_second_half_round()