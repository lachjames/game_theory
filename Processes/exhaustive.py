from explorer import compute_game
from itertools import product

import numpy as np

i = (1, 2, 3, 4)

p = 100

for vals in product(i, repeat=4):
    game = np.asarray(
        [
            [vals[0], vals[1]],
            [vals[2], vals[3]]
        ]
    )

    print(game)

    compute_game(game=game, pop_size = p)