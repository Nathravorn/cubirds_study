import numpy as np
from random import shuffle
from .utils import card_data
from .cubirds.cards import UnorderedCards
from .cubirds.game import Game
from .cubirds.game_analysis import available_lays, available_flocks

def random_turn(game):
    '''Make a random lay and flock (if one is available) action.

    Args:
        game (Game): A game of Cubirds. Current phase must be 'lay'.
    '''
    assert game.current_phase == 'lay'

    hand = game.current_hand
    board = game.board
    lays = available_lays(hand, board)
    lays = list(lays.keys())
    shuffle(lays)
    game.lay(*lays[0], draw=True)

    hand = game.current_hand
    flocks = available_flocks(hand)
    flocks = {k: v for k, v in flocks.items() if v >= 1}
    if flocks:
        flocks = list(flocks.keys())
        shuffle(flocks)
        game.flock(flocks[0])
    else:
        game.flock(None)

def playout(game):
    '''Playout a game of Cubirds with random moves until the end of the game.
    '''
    n_moves = 0
    while not game.end:
        random_turn(game)
        n_moves += 1
        # if n_moves > 40:
            # print('n_moves:', n_moves)
    return game.winner, n_moves

if __name__ == '__main__':
    game = Game(3, 4, verbose=True)
    game.state_summary()

    print(playout(game))
