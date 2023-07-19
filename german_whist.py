import random
from monte_carlo_tree_search import MCTS

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
        self.players = players
        self.player1_wins = True
        self.player1_score = 0
        self.player2_score = 0
        self.trump_card = None
        self.game_over = False
        self.trump_card = self.deck.draw_card() # trump card for the entire game


    def deal(self):
        self.player1_hand = [self.deck.draw_card() for _ in range(13)]
        self.player2_hand = [self.deck.draw_card() for _ in range(13)]
      
    def choose_card(self,player_hand, other_player_card, player):
        """
        player_hand: list of cards of current player
        other_player_card: card that was just played by previous player
        player: string, either player1 or player2
        deck: class object 
        RULES:
        Card chosen has to be the same suit as 1st played card in trick if possible
        """
        print("Your cards: ", player_hand)
        card = None
        while card not in player_hand:
            # Computer player
            if ((player == 'player2') & (self.players == 1)) :
                mcts = MCTS(simulation_limit=100)
                card = str(mcts.choose_card(player_hand))
                # card = str(player_hand[random.randint(0,len(player_hand)-1)]) # random choice of card -> good for testing
                print(f"player 2 played: {card}")
            else: # human player
                card = input("Choose a card to play: ")
            r , s = card.replace(' ','').split('of')
            card = Card(s, r)
            # # if player has the suit that was just played they have to play the suit
            if (other_player_card != None):
                if ((other_player_card.suit in [player_card.suit for player_card in player_hand]) & (card.suit != other_player_card.suit)):
                    print('illegal move')
                    card = None

        player_hand.remove(card) # remove card just played from player hand
        return card

    def play_trick(self):
        """

        """
        # to be able to compare ranks
        ranking_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, 
                        "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, 
                        "Q": 12, "K": 13, "A": 14}
        # if player1 won they start
        if self.player1_wins:
            print("Player 1's turn")
            card1 = self.choose_card(self.player1_hand, None, 'player1')
            print("Player 2's turn")
            card2 = self.choose_card(self.player2_hand, card1, 'player2')
            # reward schema for player 1 starting
            if card1.suit == card2.suit:
                self.player1_wins =  ranking_dict[card1.rank] >= ranking_dict[card2.rank]
            elif card1.suit == self.trump_card.suit: # if only player1 played a trump they win
                self.player1_wins =  True
            elif card2.suit == self.trump_card.suit: # if only player2 played a trump they win
                self.player1_wins =  False
            else: # if player2 played a different suit that isn't a trump, player1 wins
                self.player1_wins =  True

        else: # else player two starts
            print("Player 2's turn")
            card2 = self.choose_card(self.player2_hand, None, 'player2')
            print("Player 1's turn")
            card1 = self.choose_card(self.player1_hand, card2, 'player1')
            # reward schema for player 2 starting
            if card1.suit == card2.suit:
                self.player1_wins = ranking_dict[card1.rank] > ranking_dict[card2.rank]
            elif card1.suit == self.trump_card.suit:
                self.player1_wins =  True
            elif card2.suit == self.trump_card.suit:
                self.player1_wins =  False
            else:
                self.player1_wins =  False


    def play_first_half_round(self,round):
        print(f"Trump card: {self.trump_card.rank} of {self.trump_card.suit}")
        if round == 0:
            next_card = self.trump_card # first card is the trump card
        else:
            next_card = self.deck.draw_card() # draw the following card from the deck
    
        # print(f"Current round: {_}")
        print(f"\n The game trump is : {self.trump_card.suit} \n New card: {next_card}")
        self.play_trick()
        if self.player1_wins:
            print("Player 1 wins the trick.")
            self.player1_hand.append(next_card) # player 1 takes the visible card
            self.player2_hand.append(self.deck.draw_card()) # player 2 draws the top card
        else:
            print("Player 2 wins the trick.")
            self.player2_hand.append(next_card) # player 2 takes the visible card
            self.player1_hand.append(self.deck.draw_card()) # player 1 draws the top card

        # next_card = self.deck.draw_card() 

    def play_second_half_round(self):
        print(f"\nSecond half. The trump is {self.trump_card.suit}")

        # for _ in range(13):
        print("\nNew trick")
        self.play_trick()

        if self.player1_wins:
            print("Player 1 wins the trick.")
            self.player1_score += 1
        else:
            print("Player 2 wins the trick.")
            self.player2_score += 1

        print(f"\nFinal scores: Player 1: {self.player1_score}, Player 2: {self.player2_score}")
    
    # def is_game_over(self):
    #     if self.player1_hand
    #     self.game_over = False


def run_game():
    new_game = Play(players=1)
    new_game.deal()
    for _ in range(13):
        new_game.play_first_half_round(_)
    for _ in range(13):
        new_game.play_second_half_round()


if __name__ == "__main__":
    run_game()

