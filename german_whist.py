import random
from monte_carlo_tree_search import MCTS
from copy import deepcopy
import sys


def is_card_legal(card, other_player_card, player_hand):
    if (other_player_card != None):
        if ((other_player_card.suit in [player_card.suit for player_card in player_hand]) & (card.suit != other_player_card.suit)):
            # print('illegal move') 
            card = None
            return card
    return card

            

def play_lowest_card(hand, other_players_card=None):
    """
    Choose the lowest card of the required suit. 
    If there are no cards of the required suit, choose the lowest card.
    """
    ranking_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, 
                "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, 
                "Q": 12, "K": 13, "A": 14}
    
    if other_players_card is not None:
        required_suit = other_players_card.suit
        same_suit_cards = [card for card in hand if card.suit == required_suit]
        if same_suit_cards:  # If there are any cards of the required suit
            return min(same_suit_cards, key=lambda card: ranking_dict[card.rank])
    # No cards of the required suit or no suit was required, choose the lowest card
    return min(hand, key=lambda card: ranking_dict[card.rank])



class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def __eq__(self, other):
        # check if a card equals another
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in ["Spades", "Hearts", "Diamonds", "Clubs"]
                                 for r in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]]
        random.shuffle(self.cards)
        

    def draw_card(self):
        return self.cards.pop() # TODO pop breaking code

class Play:
    def __init__(self, players=1):
        self.deck = Deck()
        self.players = players # integer, number of players
        self.player1_wins = True # Player 1 always starts the game
        self.player1_score = 0 # player 1 score for second half
        self.player2_score = 0 # player 2 score for second half
        self.game_over = False
        self.trump_card = self.deck.draw_card() # trump card for the entire game
        self.next_card = self.trump_card # first drawn card is the trumpy card
        self.first_rounds_played = 0
        self.second_rounds_played = 0 
        self.card1 = None # last card played by player 1
        self.card2 = None # last card played by player 2
        self.ranking_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, 
                "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, 
                "Q": 12, "K": 13, "A": 14} # this never actually changes
        self.player1_hand = []
        self.player2_hand = []
        self.running_simulation = False

    def copy(self):
        return deepcopy(self)

    def deal(self):
        self.player1_hand = [self.deck.draw_card() for _ in range(13)]
        self.player2_hand = [self.deck.draw_card() for _ in range(13)]
      
    def choose_card(self,player_hand, other_player_card, player, card_choice=None):
        """
        player_hand: list of cards of current player
        other_player_card: card that was just played by previous player
        player: string, either player1 or player2
        
        RULES:
        Card chosen has to be the same suit as 1st played card in trick if possible
        """
        if ((self.players == 1) & (player == 'player1')) or (self.players == 2): # don't show player 2's hand to player 1
            print("Your cards: ", player_hand) if self.running_simulation == False else None
        card = None
        while card not in player_hand:
            # Computer player
            if ((player == 'player2') & (self.players == 1)):
                self.running_simulation = True
                mcts = MCTS(self,simulation_limit=100)
                legal_hand = [card for card in player_hand if is_card_legal(card, other_player_card, player_hand) is not None]
                card = str(mcts.choose_card_mcts(legal_hand))
                self.running_simulation = False
                print(f"Player 2 played: {card}") 
            #### simulated players for mcts algorithm
            elif ((player == 'player2') & (self.players == 0)):
                # player 2 plays according to a strategy
                card = str(play_lowest_card(player_hand, other_player_card))
            elif ((player == 'player1') & (self.players == 0)) :
                #when running mcts simulations player 1 chooses random cards
                card = str(player_hand[random.randint(0,len(player_hand)-1)]) # random choice of card -> good for testing
            ####
            else: # human player
                card = input("Choose a card to play: ")
            r , s = card.replace(' ','').split('of')
            card = Card(s, r)
            # # if player has the suit that was just played they have to play the suit
            card = is_card_legal(card, other_player_card, player_hand)
            if  self.running_simulation == False:
                print('Illegal card') if card == None else None
        player_hand.remove(card) # remove card just played from player hand
        return card
    


    def pay_player_1(self):
        # reward schema for player 1 starting
        if self.card1.suit == self.card2.suit:
            self.player1_wins =  self.ranking_dict[self.card1.rank] >= self.ranking_dict[self.card2.rank]
        elif self.card1.suit == self.trump_card.suit: # if only player1 played a trump they win
            self.player1_wins =  True
        elif self.card2.suit == self.trump_card.suit: # if only player2 played a trump they win
            self.player1_wins =  False
        else: # if player2 played a different suit that isn't a trump, player1 wins
            self.player1_wins =  True

    def pay_player_2(self):
        # reward schema for player 2 starting
        if self.card1.suit == self.card2.suit:
            self.player1_wins = self.ranking_dict[self.card1.rank] > self.ranking_dict[self.card2.rank]
        elif self.card1.suit == self.trump_card.suit:
            self.player1_wins =  True
        elif self.card2.suit == self.trump_card.suit:
            self.player1_wins =  False
        else:
            self.player1_wins =  False

    def play_trick(self, start_mid_round=False):
        """

        """
        # if player1 won they start
        if self.player1_wins:
            if start_mid_round:
                pass
            else:
                print("Player 1's turn") if self.running_simulation == False else None
                self.card1 = self.choose_card(self.player1_hand, None, 'player1')
            print("Player 2's turn") if self.running_simulation == False else None
            self.card2 = self.choose_card(self.player2_hand, self.card1, 'player2')
            self.pay_player_1()

        else: # else player two starts
            print("Player 2's turn") if self.running_simulation == False else None
            self.card2 = self.choose_card(self.player2_hand, None, 'player2')
            print("Player 1's turn") if self.running_simulation == False else None
            self.card1 = self.choose_card(self.player1_hand, self.card2, 'player1')
            self.pay_player_2()


    def play_first_half_round(self,round, start_mid_round = False):
        print(f"Trump card: {self.trump_card.rank} of {self.trump_card.suit}") if self.running_simulation == False else None
        if round > 0: # first round the card is the trump card
            self.next_card = self.deck.draw_card() # draw the following card from the deck
        # print(f"Current round: {_}")
        # \n The game trump is : {self.trump_card.suit} \n
        print(f"New card: {self.next_card}") if self.running_simulation == False else None
        self.play_trick(start_mid_round)
        if self.player1_wins:
            print("Player 1 wins the trick.") if self.running_simulation == False else None
            self.player1_hand.append(self.next_card) # player 1 takes the visible card
            self.player2_hand.append(self.deck.draw_card()) # player 2 draws the top card
        else:
            print("Player 2 wins the trick.") if self.running_simulation == False else None
            self.player2_hand.append(self.next_card) # player 2 takes the visible card
            self.player1_hand.append(self.deck.draw_card()) # player 1 draws the top card
        self.first_rounds_played +=1
        
        
    def play_second_half_round(self, round, start_mid_round = False):
        print(f"\nSecond half. The trump is {self.trump_card.suit}") if self.running_simulation == False else None
        # for _ in range(13):
        print("\nNew trick") if self.running_simulation == False else None
        self.play_trick(start_mid_round)

        if self.player1_wins:
            print("Player 1 wins the trick.") if self.running_simulation == False else None
            self.player1_score += 1
        else:
            print("Player 2 wins the trick.") if self.running_simulation == False else None
            self.player2_score += 1

        self.second_rounds_played +=1
        print(f"Current scores: Player 1: {self.player1_score}, Player 2: {self.player2_score}") if self.running_simulation == False else None

    def is_game_over(self):
        if (self.first_rounds_played + self.second_rounds_played == 26):
            self.game_over = True
            print('game over') if self.running_simulation == False else None


def run_game():
    players = sys.argv[1]
    if players not in ['1','2']:
        print('Player number must be between 1 and 2')
        return 'failed'
    new_game = Play(players=int(players))
    new_game.deal()
    for _ in range(13):
        print("|-------------------------------------------------|") 
        print(f'Round 1 Trick {_}')
        
        new_game.play_first_half_round(_)
    for _ in range(13):
        print("|-------------------------------------------------|") 
        print(f'Round 2 Trick {_}')
        
        new_game.play_second_half_round(_)
    new_game.is_game_over()


if __name__ == "__main__":
    run_game()

