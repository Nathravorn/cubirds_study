import multiprocessing as mp

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from tqdm import tqdm

from cubirds.game import Game
from random_moves import playout

def build_srs_iter(_):
    game = Game(3, 4, verbose=False)
    _, n_moves = playout(game)
    return n_moves

def build_n_moves_srs(n=500):
    with mp.Pool(8) as pool:
        srs = list(tqdm(pool.imap(build_srs_iter, range(n)), total=n))
    # srs = [build_srs_iter(i) for i in tqdm(range(n))]
    srs = pd.Series(srs)
    return srs

if __name__ == '__main__':
    srs = build_n_moves_srs(20000)
    print(srs.describe())
    sns.distplot(srs)
    plt.show()
