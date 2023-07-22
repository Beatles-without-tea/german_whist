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