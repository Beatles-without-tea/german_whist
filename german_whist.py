import random

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
    def __init__(self, players = 2):
        self.cards = [Card(s, r) for s in ["Spades", "Hearts", "Diamonds", "Clubs"]
                                 for r in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]]
        random.shuffle(self.cards)
        self.players = players

    def draw_card(self):
        return self.cards.pop() # TODO pop breaking code

def deal(deck):
    player1_hand = [deck.draw_card() for _ in range(13)]
    player2_hand = [deck.draw_card() for _ in range(13)]
    return player1_hand, player2_hand

def choose_card(player_hand, other_player_card, player, deck):
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
        # bot that plays randomly
        if ((player == 'player2') & (deck.players == 1)) :
            card = str(player_hand[random.randint(0,len(player_hand))])
            print(f"player 2 played: {card}")
        else:
            card = input("Choose a card to play: ")
        r , s = card.replace(' ','').split('of')
        card = Card(s, r)
        # # if player has the suit they have to play the suit
        if (other_player_card != None):
            if ((other_player_card.suit in [player_card.suit for player_card in player_hand]) & (card.suit != other_player_card.suit)):
                print('illegal move')
                card = None

    player_hand.remove(card)
    return card

def play_trick(player1_hand, player2_hand, trump, player1_wins,deck):
    """

    """
    # to be able to compare ranks
    ranking_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, 
                    "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, 
                    "Q": 12, "K": 13, "A": 14}
    # if player1 won they start
    if player1_wins:
        print("Player 1's turn")
        card1 = choose_card(player1_hand, None, 'player1',deck)
        print("Player 2's turn")
        card2 = choose_card(player2_hand, card1, 'player2',deck)
        # reward schema for player 1 starting
        if card1.suit == card2.suit:
            return card1, card2, ranking_dict[card1.rank] >= ranking_dict[card2.rank]
        elif card1.suit == trump.suit:
            return card1, card2, True
        elif card2.suit == trump.suit:
            return card1, card2, False
        else:
            return card1, card2, True

    else: # else player two starts
        print("Player 2's turn")
        card2 = choose_card(player2_hand, None, 'player2')
        print("Player 1's turn")
        card1 = choose_card(player1_hand, card2, 'player1')
        # reward schema for player 2 starting
        if card1.suit == card2.suit:
            return card1, card2, ranking_dict[card1.rank] <= ranking_dict[card2.rank]
        elif card1.suit == trump.suit:
            return card1, card2, True
        elif card2.suit == trump.suit:
            return card1, card2, False
        else:
            return card1, card2, False



def play_first_half(player1_hand, player2_hand, deck):
    trump_card = deck.draw_card()
    print(f"Trump card: {trump_card.rank} of {trump_card.suit}")
    next_card = trump_card # first card is the trump card
    player1_wins = True # start new games with player 1 (No dealer)
    for _ in range(13):
        print(f"Current round: {_}")
        print(f"\n The game trump is : {trump_card.suit} \n New card: {next_card}")
        card1, card2, player1_wins = play_trick(player1_hand, player2_hand, trump_card, player1_wins,deck)

        if player1_wins:
            print("Player 1 wins the trick.")
            player1_hand.append(next_card) # player 1 takes the visible card
            player2_hand.append(deck.draw_card()) 
        else:
            print("Player 2 wins the trick.")
            player2_hand.append(next_card) # player 2 takes the visible card
            player1_hand.append(deck.draw_card()) # player 2 draws the top card

        next_card = deck.draw_card() # draw the following card from the deck
    return player1_wins, trump_card

def play_second_half(player1_hand, player2_hand, trump_card, player1_wins):
    player1_score, player2_score = 0, 0

    for _ in range(13):
        print("\nNew trick")
        card1, card2, player1_wins = play_trick(player1_hand, player2_hand, trump_card, player1_wins)

        if player1_wins:
            print("Player 1 wins the trick.")
            player1_score += 1
        else:
            print("Player 2 wins the trick.")
            player2_score += 1

    print(f"\nFinal scores: Player 1: {player1_score}, Player 2: {player2_score}")

def main():
    deck = Deck(players=1)
    player1_hand, player2_hand = deal(deck)
    player1_wins, trump_card = play_first_half(player1_hand, player2_hand, deck)
    print(f"\nSecond half. The trump is {trump_card.suit}")
    play_second_half(player1_hand, player2_hand, trump_card, player1_wins)

if __name__ == "__main__":
    main()
