from random import shuffle
import json
import numpy as np
import pandas as pd
from utils import card_data, count_hand, list_hand


class Stack:
    '''An unordered stack of cards. Has a dict form (self.d) and a list form.
    Both can be used to update the stack. Supports subscripting to get and set
    card counts.
    Example:
        stack = Stack(['cube', 'cube'])
        stack['sandwich'] += 1
    '''
    def __init__(self, stack=[]):
        '''Initialize a stack with a list of strings. All strings must be valid
        card types.
        '''
        if isinstance(stack, list):
            self.d = count_hand(stack)
        elif isinstance(stack, dict):
            self.d = stack
        elif isinstance(stack, Stack):
            self.d = stack.d.copy()
        else:
            raise Exception('Stack initializer must be list, dict or stack.')

    def standardize_input(self, input, target='list'):
        '''Standardize input lists or dicts to one target.
        '''
        if isinstance(input, list):
            if target == 'list':
                return input
            elif target == 'dict':
                return count_hand(input)
        elif isinstance(input, dict):
            if target == 'list':
                return list_hand(input)
            elif target == 'dict':
                return input
        elif isinstance(input, Stack):
            if target == 'list':
                return input.l
            elif target == 'dict':
                return input.d
        else:
            raise Exception('Unrecognized input type.')

    def __str__(self):
        return json.dumps(self.d, indent=4, sort_keys=True)

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    def get_list(self):
        return list_hand(self.d)

    def set_list(self, new_list):
        self.d = count_hand(new_list)

    l = property(get_list, set_list)

    def __len__(self):
        return len(self.l)

    def __add__(self, other):
        other = self.standardize_input(other, 'list')
        out = self.l + other
        return Stack(out)

    def __sub__(self, other):
        other = self.standardize_input(other, 'dict')
        out = self.d.copy()
        for bird in out:
            sub = self[bird] - other[bird]
            if sub < 0:
                raise Exception('Cannot subtract {} {}s from {}'.format(other[bird], bird, self[bird]))
            else:
                out[bird] = sub
        return Stack(out)

    def draw(self, n=1):
        out = list(np.random.choice(self.l, min(n, len(self)), replace=False))
        self.d = (self - out).d

        return Stack(out)

    def dedupe(self):
        '''Separate the stack into its unique elements and any extra duplicates.
        Returns:
            Stack: a stack containing only unique cards.
            Stack: a stack containing only extra duplicates.
        '''
        dupes = Stack()
        for bird, count in self.d.items():
            if count >= 2:
                self.d[bird] = 1
                dupes.d[bird] = count - 1

        return self, dupes

def get_deck():
    '''Return a Stack of all 110 cards in the game.
    '''
    deck = {bird: atts['count'] for bird, atts in card_data.items()}

    return Stack(deck)


# stack = Stack(list('abcabc'))
# hand = stack.draw(10)
#
# print(stack, hand)
