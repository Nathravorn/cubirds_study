from random import shuffle
import json
import numpy as np
import pandas as pd
from utils import card_data

card_data = list('abc')

class Stack:
    '''A stack of cards. Has a dict form (self.d) and a list form. Both can be
    used to update the stack. Supports subscripting to get and set card counts
    Example:
        stack = Stack(['cube', 'cube'])
        stack['sandwich'] += 1
    '''
    def __init__(self, stack=[]):
        '''Initialize a stack with a list of strings. All strings must be valid
        card types.
        '''
        if isinstance(stack, list):
            self.update_d(stack)
        elif isinstance(stack, dict):
            self.d = stack
        elif isinstance(stack, Stack):
            self.d = stack.d
        else:
            raise Exception('Stack initializor must be list, dict or stack.')

    def __str__(self):
        return json.dumps(self.d, indent=4, sort_keys=True)

    def update_d(self, list_form):
        self.d = {bird: 0 for bird in card_data}
        self.d.update(
            {b: int(c) for b, c in zip(*np.unique(list_form, return_counts=True))}
            )

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    def get_list(self):
        out = []
        for bird in sorted(self.d):
            out.extend([bird]*self.d[bird])
        return out

    def set_list(self, new_list):
        self.update_d(new_list)

    l = property(get_list, set_list)

    def __len__(self):
        return len(self.l)

    def shuffle(self):
        self.

    def add(self, other):
        if isinstance(other, Stack):
            other = other.l
        stack = self.l + other
        return Stack(stack)

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

# stack = Stack(list('abc'))
# stack['a'] += 1
# print(*stack.dedupe())
