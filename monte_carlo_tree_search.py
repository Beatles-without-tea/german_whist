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
    def __init__(self, simulation_limit):
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
        print('state: ',node.state)
        # Add all possible moves as children
        for card in node.state:
            new_state = node.state[:]  # Copy the current state
            new_state.remove(card)  # Remove the played card
            node.children.append(Node(new_state, parent=node, action=card))
           
        print('loop finished')

    def simulation(self, node):
        # TODO -> returns winner of game
        return random.choice([0, 1])

    def backpropagation(self, node, result):
        # Propagate the result up to the root
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    def choose_card(self, current_state):
        root = Node(current_state)
        for _ in range(self.simulation_limit):
            print("simulation: ", _)
            leaf = self.selection(root)
            print('leaf: ', leaf)
            self.expansion(leaf)
            result = self.simulation(leaf)
            self.backpropagation(leaf, result)
        return max(root.children, key=lambda c: c.wins/c.visits).state

# new_game = Play(players=1)
# new_game.deal()
# for _ in range(13):
#     new_game.play_first_half_round()
# for _ in range(13):
#     new_game.play_second_half_round()