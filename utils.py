import numpy as np
import json
# import pydealer

def json_print(d):
    print(json.dumps(d, indent=4, sort_keys=True))

with open('card_data.json', 'r') as file:
    card_data = json.load(file)

def get_bird_df():
    '''Return a dataframe containing common stats about each bird.
    '''
    df = (pd.DataFrame.from_dict(card_data, orient='index')
        .sort_values('count', ascending=False)
        .eval('s_ratio = small / count')
        .eval('b_ratio = big / count'))

    return df

# print(get_deck())
