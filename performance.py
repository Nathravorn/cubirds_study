from timeit import default_timer as dt

from game import Game
from game_analysis import available_lays, available_flocks
from random_moves import playout



def test_available_lays():
    game = Game(1, 4)
    hand = game.current_hand
    board = game.board
    start = dt()
    for _ in range(1000):
        available_lays(hand, board)
    print((dt()-start)/1000)

def test_playout(n_tests=500):
    elapsed = lambda x: (dt() - x) / n_tests
    
    start = dt()
    for _ in range(n_tests):
        Game(3, 4, verbose=False)
    print(f'Time to create a game: {elapsed(start)}')
    
    start = dt()
    for i in range(n_tests):
        game = Game(3, 4, verbose=False)
    print(f'Time to create and play: {elapsed(start)}')
    
if __name__ == '__main__':
    # test_available_lays()
    test_playout(1000)