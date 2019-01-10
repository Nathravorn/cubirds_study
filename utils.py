import numpy as np
import json
# import pydealer

with open('card_data.json', 'r') as file:
    card_data = json.load(file)

# card_data = list('abc')

def json_print(d):
    print(json.dumps(d, indent=4, sort_keys=True))

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
