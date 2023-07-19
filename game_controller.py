from german_whist import Play
from monte_carlo_tree_search import MCTS

class GameController:
    def __init__(self):
        self.play = Play()
        self.mcts = MCTS(100)

    def run_game(self):
        new_game = Play(players=1)
        new_game.deal()
        for _ in range(13):
            new_game.play_first_half_round(_)
        for _ in range(13):
            new_game.play_second_half_round()

GameController().run_game()