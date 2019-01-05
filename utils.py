import numpy as np
import pandas as pd
import json
# import pydealer

with open('card_data.json', 'r') as file:
    card_data = json.load(file)

# card_data = list('abc')


def count_hand(hand):
    '''Count the unique cards in a list of cards (hand).
    Args:
        hand (list): list of strings. All strings must be valid bird names.
    Returns:
        dict: name->count dictionary. Includes birds which appear 0 times.
    '''
    count = {bird: 0 for bird in card_data}
    count.update({k: int(v) for k, v in zip(*np.unique(hand, return_counts=True))})
    return count

def list_hand(hand):
    '''Revert a counted hand to a list of strings.
    Args:
        dict: name->count dictionary.
    Returns:
        hand (list): list of strings.
    '''
    cards = []
    for bird in hand:
        cards.extend([bird]*hand[bird])

    return cards

def dedupe(hand):
    '''Separate a dict-form hand into its unique elements and any extra
    duplicates.
    Args:
        hand (dict): counted hand.
    Returns:
        dict: a hand containing only unique cards.
        dict: a hand containing only extra duplicates.
    '''
    dupes = count_hand([])
    for bird, count in hand.items():
        if count >= 2:
            hand[bird] = 1
            dupes[bird] = count - 1

    return hand, dupes

def get_bird_df():
    '''Return a dataframe containing common stats about each bird.
    '''
    df = (pd.DataFrame.from_dict(card_data, orient='index')
        .sort_values('count', ascending=False)
        .eval('s_ratio = small / count')
        .eval('b_ratio = big / count'))

    return df

# print(get_deck())
