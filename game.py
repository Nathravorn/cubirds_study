import numpy as np
import pandas as pd
from random import shuffle

from utils import card_data
from stack import Stack, get_deck

class Game:
    def __init__(self, n_players=4):
        self.n_players = n_players
        self.current_turn = 0
        self.current_player = 0

        self.deck = get_deck()
        self.discard = Stack()
        self.hands = self.init_hands()
        self.collections = self.init_collections()
        self.board = self.init_board()

        self.end = False
        self.winner = None

    def draw(self, n=1):
        '''Removes the first n cards from the deck and returns them.
        If draw is impossible, draws until deck is empty, then shuffles the
        discard pile into the deck.
        '''
        if len(self.deck) >= n:
            hand = self.deck.draw(n)
        else:
            if len(self.deck) + len(self.discard) >= n:
                hand = self.deck
                self.deck = self.discard
                self.discard = Stack()
                hand = hand + self.draw(n-len(hand))
            else:
                raise Exception('Cannot draw {} from {}'.format(n,
                                len(self.deck) + len(self.discard)))

        return hand

    def init_hands(self):
        hands = {}
        for player in range(self.n_players):
            hands[player] = self.draw(8)

        return hands

    def init_collections(self):
        collections = {}
        for player in range(self.n_players):
            collections[player] = self.draw(1)

        return collections

    def init_board(self):
        board = {}
        for n_row in range(4):
            row = self.draw(3)
            while row.n_unique() < 3:
                row, dupes = row.dedupe()
                self.discard += dupes
                row += self.draw(1)
            board[n_row] = row

        return board

    def state_summary(self):
        def indent_string(s):
            return '    '+s.replace('\n', '\n    ')

        def title(s):
            return s + '\n' + '='*len(s) + '\n'

        out = [
            'Current turn: {}'.format(self.current_turn),
            'Current player: {}'.format(self.current_player),
            '',
            'Deck:',
            indent_string(str(self.deck)),
            '\n\n'
        ]

        for player in range(self.n_players):
            out.extend([
                'Player {}:'.format(player),
                '    Hand: ' + ', '.join(self.hands[player].l),
                '    Collection: ' + ', '.join(self.collections[player].l)
            ])

        out.extend([
            '\n\n',
            'Board:'
        ])

        for n_row in range(4):
            out.append('Row {}: '.format(n_row) + ', '.join(self.board[n_row].l))

        return '\n'.join(out)

if __name__ == '__main__':
    game = Game(2)
    print(game.state_summary())
