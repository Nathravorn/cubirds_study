import pytest

from cubirds.game import Game
from cubirds.stack import Stack
from cubirds.game_analysis import available_lays, available_flocks
from random_moves import playout


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

