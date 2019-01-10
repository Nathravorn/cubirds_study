import pytest

from cubirds.game import Game
from cubirds.stack import Stack
from cubirds.game_analysis import available_lays, available_flocks
from random_moves import playout


def test_game_example():
    game = Game(n_players=1, n_rows=1)
    game.deck = Stack(['sparrow'])
    game.board[0] = ['parrot', 'parrot', 'parrot', 'parrot', 'cube']
    game.hands[0] = Stack(['cube', 'cube', 'sandwich'])
    assert game.current_phase == 'lay'

    game.lay('cube', 0, 'left')
    assert game.current_phase == 'flock'
    assert game.deck.l == []
    assert game.board[0] == ['cube', 'cube', 'cube', 'sparrow']

    game.flock('parrot')
    assert game.current_phase == 'lay'
    assert game.hands[0].l == ['sandwich']
    assert 'parrot' in game.collections[0].l

def test_perf_available_lays(benchmark):
    game = Game(1, 4)
    hand = game.current_hand
    board = game.board
    benchmark(available_lays, hand, board)

def test_perf_create_game(benchmark):
    def create():
        Game(3, 4, verbose=False)
    benchmark(create)

def test_perf_playout(benchmark):
    def create_and_play():
        game = Game(3, 4, verbose=False)
        # TODO: play
    benchmark(create_and_play)

