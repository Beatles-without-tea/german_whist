def play_optimal_strategy(hand, 
                    first_rounds_played, 
                    second_rounds_played,
                    trump_card=None,  
                    next_card=None,
                    other_players_card=None):
    """

    """
    ranking_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, 
                    "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, 
                    "Q": 12, "K": 13, "A": 14}

    # In the first half of the game, prioritize winning cards
    if first_rounds_played < 13:
        if ((next_card.suit == trump_card.suit) or (ranking_dict[next_card.rank]>7)): # decide if we want the card
            if other_players_card is not None: #
                same_suit_cards = [card for card in hand if card.suit == other_players_card.suit]
                winning_cards = [card for card in same_suit_cards if ranking_dict[card.rank] > ranking_dict[other_players_card.rank]]
                losing_cards = [card for card in same_suit_cards if ranking_dict[card.rank] <= ranking_dict[other_players_card.rank]]
                if winning_cards:
                    smallest_winner = min(winning_cards, key=lambda card: ranking_dict[card.rank])
                    # if it's a trump suit always win it if our card is not of the suit
                    if ((next_card.suit == trump_card.suit) & (smallest_winner.suit != trump_card.suit)) :
                        return smallest_winner
                    # if not trump suit or rank is same as smallest winner, don't play a higher rank than the card that will be won
                    elif (smallest_winner.rank > next_card.rank) : 
                        return min(losing_cards, key=lambda card: ranking_dict[card.rank])
            
            if other_players_card is None: #
                highest_card = max(hand, key=lambda card: ranking_dict[card.rank])
                # if the suit of next card is trump, and the highest card isn't a trump take the card
                if ((next_card.suit == trump_card.suit) & (highest_card.suit != trump_card.suit)) :
                    return highest_card

                else:
                    sorted_cards = sorted(hand, key=lambda card: ranking_dict[card.rank])
                    for card in sorted_cards:
                        if ranking_dict[card.rank] < ranking_dict[next_card.rank]:
                            return card
                    

                    return min(other_suit_cards, key=lambda card: ranking_dict[card.rank])

    # In the second half of the game, prioritize winning with trump cards
    elif second_rounds_played < 13:
        # If we have the trump suit, play the lowest trump that can still win
        if trump_suit is not None:
            trump_cards = [card for card in hand if card.suit == trump_suit]
            if trump_cards:
                winning_trumps = [card for card in trump_cards if ranking_dict[card.rank] > ranking_dict.get(other_players_card.rank, 0)]
                if winning_trumps:
                    return min(winning_trumps, key=lambda card: ranking_dict[card.rank])

    # If we can't win, or it's the second half of the game, sacrifice the lowest value card
    if other_players_card is not None:
        required_suit = other_players_card.suit
        other_suit_cards = [card for card in hand if card.suit != required_suit]
        if other_suit_cards:
            return min(other_suit_cards, key=lambda card: ranking_dict[card.rank])

    # No cards of the required suit or no suit was required, choose the lowest card
    return min(hand, key=lambda card: ranking_dict[card.rank])
