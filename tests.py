from german_whist import Play

def test_0_player_game():
    players = 0
    new_game = Play(players=players)
    new_game.deal()
    new_game.player2_hand
    for _ in range(13):
        new_game.play_first_half_round(_)
        assert len(new_game.player1_hand) == 13
        assert len(new_game.player2_hand) == 13
    for j in range(13):
        assert len(new_game.player1_hand) == 13 - j
        assert len(new_game.player2_hand) == 13 - j
        new_game.play_second_half_round(_)


