def play_optimal_strategy(hand, 
                    first_rounds_played, 
                    second_rounds_played,
                    trump_card,  
                    next_card,
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
                if len(same_suit_cards) == 0: # we don't have any same suit cards
                    winning_cards = [card for card in hand if ranking_dict[card.rank] > ranking_dict[other_players_card.rank]]
                    losing_cards = [card for card in hand if ranking_dict[card.rank] <= ranking_dict[other_players_card.rank] and card.suit != trump_card.suit]
                else: # we have same suit cards
                    winning_cards = [card for card in same_suit_cards if ranking_dict[card.rank] > ranking_dict[other_players_card.rank]]
                    losing_cards = [card for card in same_suit_cards if ranking_dict[card.rank] <= ranking_dict[other_players_card.rank] and card.suit != trump_card.suit]

                if winning_cards:
                    smallest_winner = min(winning_cards, key=lambda card: ranking_dict[card.rank])
                    smallest_loser = min(losing_cards, key=lambda card: ranking_dict[card.rank])
                    # if it's a trump suit always win it if our card is not of the suit
                    if ((next_card.suit == trump_card.suit) & (smallest_winner.suit != trump_card.suit)) :
                        return smallest_winner
                    # if not trump suit or rank is same as smallest winner, don't play a higher rank than the card that will be won
                    elif (smallest_winner.rank > next_card.rank) : 
                        return smallest_loser
            
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

    # In the second half of the game, prioritize winning with trump cards
    elif second_rounds_played < 13:
        if other_players_card is not None:
            same_suit_cards = [card for card in hand if card.suit == other_players_card.suit]
            if len(same_suit_cards) == 0: # if no same suit cards play a trump and win
                # play the lowest trump 
                trump_cards = [card for card in hand if card.suit == trump_card.suit]
                if trump_cards:
                    return min(trump_cards, key=lambda card: ranking_dict[card.rank])
                else: # if no trumps you lose in any case so use smallest
                    return min(hand, key=lambda card: ranking_dict[card.rank])
        if other_players_card is None:
            non_trump_cards = [card for card in hand if card.suit != trump_card.suit]
            trump_cards = [card for card in hand if card.suit == trump_card.suit]
            
            if non_trump_cards:  # If there are any non-trump cards
                return max(non_trump_cards, key=lambda card: ranking_dict[card.rank])
            else:
                return max(trump_cards, key=lambda card: ranking_dict[card.rank]) 
        
    # No cards of the required suit or no suit was required, choose the lowest card
    return min(hand, key=lambda card: ranking_dict[card.rank])
