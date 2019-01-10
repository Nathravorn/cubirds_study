from random import shuffle
from multiset import Multiset
import json
import numpy as np
from ..utils import card_data


class Stack:
    '''An unordered stack of cards. Has a dict form (self.d) and a list form.
    Both can be used to update the stack. Supports subscripting to get and set
    card counts, as well as +, - and 'in' operators to combine stacks together.

    Example:
        stack = Stack(['cube', 'cube'])
        stack['sandwich'] += 1
        stack += ['cube', 'sparrow']
        stack -= ['sparrow']
        stack.draw_all('cube')
        print(stack.l)
        # ['sandwich']

    Attributes:
        d (dict): self dict-form. Keys are card types and values are counts.
                  Includes card types which appear 0 times.
    '''
    def __init__(self, stack=[]):
        '''Initialize a stack with either a list of strings, a dict-form stack
        or another Stack object.

        Args:
            stack (list, dict or Stack): card stack representation.
        '''
        if isinstance(stack, Stack):
            self.d = stack.d.copy()
        else:
            self.d = Multiset(stack)

    def extract_multiset(self, input):
        '''Standardize input lists or dicts to one target.
        '''
        if isinstance(input, Stack):
            return input.d
        else:
            return Multiset(input)

    def __str__(self):
        out = {k: v for k, v in self.items() if v > 0}
        return json.dumps(out, indent=4, sort_keys=True)

    def __repr__(self):
        out = {k: v for k, v in self.items() if v > 0}
        return str(out)

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    def get_list(self):
        return list(iter(self.d))

    def set_list(self, new_list):
        self.d = Multiset(new_list)

    l = property(get_list, set_list)

    @property
    def empty(self):
        return self.l == []

    def n_unique(self):
        '''Number of unique card types which appear at least once in the stack.
        '''
        return len(set(self.l))

    def __len__(self):
        return len(self.d)

    def __contains__(self, other):
        return other in self.d

    def __add__(self, other):
        other = self.extract_multiset(other)
        return Stack(self.d + other)

    def __sub__(self, other):
        other = self.extract_multiset(other)
        return Stack(self.d - other)

    def draw(self, n=1):
        '''Draw n random cards from self and return them.
        '''
        out = []
        l = len(self)
        birds = list(self.d.distinct_elements())
        for _ in range(n):
            if l == 0:
                break
            selected_bird = np.random.choice(birds, p=[self[k]/l for k in birds])
            out.append(selected_bird)
            self[selected_bird] -= 1
            l -= 1

        return Stack(out)

    def draw_all(self, bird):
        '''Draw all cards of type bird from self and return them.
        '''
        out = [bird] * self[bird]
        self[bird] = 0
        return Stack(out)

    def dedupe(self):
        '''Separate the stack into its unique elements and any extra duplicates.
        Returns:
            Stack: a stack containing only unique cards.
            Stack: a stack containing only extra duplicates.
        '''
        dupes = Stack()
        for bird, count in self.items():
            if count >= 2:
                self[bird] = 1
                dupes[bird] = count - 1

        return self, dupes

    def to_dict(self):
        return { k:v for k, v in self.d.items() }

    def items(self):
        return self.d.items()

    def values(self):
        return self.d.values()

def get_deck():
    '''Return a Stack of all 110 cards in the game.
    '''
    deck = {bird: atts['count'] for bird, atts in card_data.items()}

    return Stack(deck)


# if __name__ == '__main__':
    # stack = Stack(list('abcabc'))
    # hand = stack.draw(10)
    #
    # print(stack, hand)

    # print(list('abcaa') in stack)
