import itertools as it
from timeit import default_timer as dt
import numpy as np

from ..utils import card_data, json_print
from .cards import UnorderedCards
from .game import Game


def compute_lay(bird, row, side):
    '''Computes what a player will draw by laying birds of type 'bird' on a
    given side of a given row.

    Args:
        bird (str): A valid bird name.
        row (list): A list of valid bird names.
        side (str): 'left' or 'right'. The side to lay on.
    '''
    # For the sake of readability, we assume that cards are always put on
    # the right of the row. If the left is chosen, we reverse the row at the
    # start then reverse it again at the end of the process.
    row = row if side == 'right' else list(reversed(row))

    bird_ix = [i for i, x in enumerate(row) if x == bird]

    # If the bird is absent from the row or is present at the very right, the
    # outcome depends on the player's draw choice.
    if (not bird_ix) or (len(row) - 1 in bird_ix):
        return 'draw'
    else:
        return row[bird_ix[-1]+1:]

def available_lays(hand, board):
    '''Lists all possible lays by a player with a given hand on a given board,
    and computes their outcomes.

    Args:
        hand (UnorderedCards, list or dict): A hand of cards.
        board (dict of lists of strings): The rows of the board.

    Returns:
        dict: A nested dictionary with (bird, row, side) as keys and UnorderedCardss as
            values.
    '''
    hand = UnorderedCards(hand)
    out = {}
    for bird in set(hand.l):
        for n_row, row in board.items():
            for side in ['left', 'right']:
                out[(bird, n_row, side)] = compute_lay(bird, row, side)

    return out

def available_flocks(hand):
    '''Given a hand of cards, returns a dict of flock possibilities.
    Args:
        hand (UnorderedCards, list or dict): A hand of cards.
    Returns:
        dict: A dictionary with card types as keys and either 0 (no flock), 1
             (small flock) or 2 (big flock) as values.
    '''
    hand = UnorderedCards(hand)
    out = {}
    for bird, count in hand.items():
        if count >= card_data[bird]['big']:
            out[bird] = 2
        elif count >= card_data[bird]['small']:
            out[bird] = 1
        else:
            out[bird] = 0
    return out

def flocks_to_list(flock_dict):
    '''Turns a flock dict (with card types as keys and either 0 (no flock), 1
    (small flock) or 2 (big flock) as values) into a list of flock options
    denoted as e.g. 'small_sparrow'

    Args:
        flock_dict: output of available_flocks()

    Returns:
        flock_list: a list of flock options.
    '''
    out = []
    for bird, flock in flock_dict.items():
        if flock == 2:
            out.append('{}_{}'.format('big', bird))
        elif flock == 1:
            out.append('{}_{}'.format('small', bird))
    return sorted(out)

def available_moves(game, counts='deck'):
    '''Lists all legal moves the current player can make at the start of his
    turn.

    Args:
        game (Game): A game of Cubirds. game.current_phase should be 'lay' for
            the use of this function to make sense, but it will work regardless.
        counts (str or dict): How many of each bird are in the deck.
            If 'deck', uses the base probabilities in the deck.
            If 'invisible', uses the card proportion in cards invisible to the player.
            If dict, implements custom class probabilities.
    '''
    if counts == 'deck':
        counts = {}
        for bird, info in card_data.items():
            counts[bird] = info['count']
    elif counts == 'invisible':
        counts = game.invisible(game.current_player).to_dict()

    counts['total'] = sum(counts.values())

    draw_probas = {}
    for draw in it.product(card_data, card_data):
        same = draw[0] == draw[1]
        draw_probas[draw] = (
              counts[draw[0]]
            / counts['total']
            * (counts[draw[1]] - (1 if same else 0))
            / (counts['total'] - 1)
        )

    out = {}
    for lay_option, cards in available_lays(game.current_hand, game.board).items():
        hand = UnorderedCards(game.current_hand)
        hand.draw_all(lay_option[0])
        if cards == 'draw':
            proba_map = {}
            for draw in it.product(card_data, card_data):
                flocks = tuple(flocks_to_list(available_flocks(hand + list(draw))))

                if flocks in proba_map:
                    proba_map[flocks] += draw_probas[draw]
                else:
                    proba_map[flocks] = draw_probas[draw]
            # proba_map = {k: v/64 for k, v in proba_map.items()}
            out[lay_option] = proba_map

        else:
            out[lay_option] = tuple(flocks_to_list(available_flocks(hand + cards)))

    return out

def print_available_moves(am):
    d = {}
    for lay_option, outcome in am.items():
        if isinstance(outcome, dict):
            outcome = {str(k): v for k, v in outcome.items()}
        d[str(lay_option)] = outcome
    json_print(d)


if __name__ == '__main__':
    # hand = ['cube', 'sandwich']
    # board = {
    #     0: ['cube', 'sparrow', 'sparrow'],
    #     1: ['sandwich', 'cube', 'sparrow']
    # }
    # print(available_lays(hand, board))

    game = Game(n_players=1, n_rows=4)
    print(game.state_summary())
    am = available_moves(game)
    print_available_moves(am)
