from german_whist import Play, is_card_legal, Card

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
    # check game over
    # check that a player won


def test_payouts():
    new_game = Play(players=0)
    new_game.trump_card = Card('Spades','2')
    new_game.card1 = Card('Diamonds','K')
    new_game.card2 = Card('Spades','1')
    new_game.pay_player_1()
    assert new_game.player1_wins == False






# check cards (equality and rankings)
# make sure payments are correct
# test card legality