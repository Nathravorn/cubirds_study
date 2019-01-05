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
            hand = self.deck[:n]
            self.deck = self.deck[n:]
        else:
            if len(self.deck) + len(self.discard) >= n:
                hand = self.deck
                self.deck = self.discard
                shuffle(self.deck)
                self.discard = []
                hand.extend(draw(n-len(hand)))
            else:
                raise Exception('Cannot draw {} from {}'.format(n,
                                len(self.deck) + len(self.discard)))

    def init_hands(self):
        hands = {}
        for player in range(self.n_players):
            hands[player] = count_hand(self.draw(8))

        return hands

    def init_collections(self):
        collections = {}
        for player in range(self.n_players):
            collections[player] = count_hand(self.draw(1))

        return collections

    def init_board(self):
        board = {}
        for n_row in range(4):
            row = self.draw(3)
            while len(set(row)) < 3:


        return board

game = Game(2)

print(len(game.deck))
print(game.hands)
print(game.collections)
