from math import sqrt, log
import random
from tqdm import tqdm

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state  #  Player 2's hand
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.action = action  

class MCTS:
    def __init__(self, play , simulation_limit ):
        self.play = play
        self.simulation_limit = simulation_limit
        
    def UCT(self, node):
        if node.visits == 0:
            return float('inf')  # prioritize unvisited nodes
        else:
            return node.wins / node.visits + sqrt(2) * sqrt(log(node.parent.visits) / node.visits)

    def selection(self, node):
        while node.children:
            node = max(node.children, key=self.UCT)
        return node


    def expansion(self, node):
        # Add all possible moves as children
        for card in node.state:
            new_state = node.state[:]  # copy the current state
            new_state.remove(card)  # remove the played card
            node.children.append(Node(new_state, parent=node, action=card))
           
    def simulation(self, node):
        """
        Run a simulated game to the end of the second phase, then return the result.
        """
        simulated_game = self.play.copy()
        simulated_game.players = 0
        # play out the game here until the end of the second phase     
        # first round is a half round, the simulation starts at the current point in the game
        if ((simulated_game.player1_wins) & (simulated_game.first_rounds_played < 12)):
            simulated_game.play_first_half_round(13 - simulated_game.first_rounds_played, start_mid_round=True)
        for _ in range( 13 - simulated_game.first_rounds_played-1):
            simulated_game.play_first_half_round(_)
        if ((simulated_game.player1_wins) & (simulated_game.second_rounds_played < 12)):
            simulated_game.play_second_half_round(13 - simulated_game.second_rounds_played, start_mid_round=True)
        for _ in range( 13 - simulated_game.second_rounds_played -1 ):
            simulated_game.play_second_half_round(_)

        # payout scores
        if simulated_game.player2_score > simulated_game.player1_score:
            return 1  # Player 2 wins
        else:
            return 0  # Player 2 does not win


    def backpropagation(self, node, result):
        # Propagate the result up to the root
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    def choose_card_mcts(self, current_state):
        root = Node(current_state)
        for _ in tqdm(range(self.simulation_limit)):
            leaf = self.selection(root)
            self.expansion(leaf)
            result = self.simulation(leaf)
            self.backpropagation(leaf, result)
        return max(root.children, key=lambda c: c.wins/c.visits).action


# todo improve strategy
