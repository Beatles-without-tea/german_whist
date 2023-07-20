from math import sqrt, log
import random



class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state  # This is the hand of Player 2
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
        # The UCT formula is usually: average reward + exploration factor * sqrt(log(total parent visits) / node visits)
        # The exploration factor balances between exploration and exploitation. We'll use sqrt(2) as a common choice.
        if node.visits == 0:
            return float('inf')  # Prioritize unvisited nodes
        else:
            return node.wins / node.visits + sqrt(2) * sqrt(log(node.parent.visits) / node.visits)

    def selection(self, node):
        while node.children:
            node = max(node.children, key=self.UCT)
        return node


    def expansion(self, node):
        # Add all possible moves as children
        for card in node.state:
            new_state = node.state[:]  # Copy the current state
            new_state.remove(card)  # Remove the played card
            node.children.append(Node(new_state, parent=node, action=card))
           
        # print('loop finished')




    def simulation(self, node):
        # improve strategy for player 2
        
    
        """
        Run a simulated game to the end of the second phase, then return the result.
        """
        print('running simulation')
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
        for _ in range( 13 - simulated_game.second_rounds_played):
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
        for _ in range(self.simulation_limit):
            print("simulation: ", _)
            leaf = self.selection(root)
            self.expansion(leaf)
            result = self.simulation(leaf)
            self.backpropagation(leaf, result)
        print('simulations over')
        return max(root.children, key=lambda c: c.wins/c.visits).action


# todo improve strategy
# todo second round half start?
# fix almost infinite loop thing?
# remove print statements for simulations and # fix output 
# make tests
# make terminal commands to run game, with flags ex player-1 etc
#