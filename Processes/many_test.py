from many import Many, random_game, r
from wright_fisher import Wright_Fisher
from moran import Moran

import itertools

models = {"wf": Wright_Fisher, "moran": Moran}

TRIALS = 1

n, a, b = 3, 2, 4

w_values = [0.001, 0.1, 1]
num_players = [2, 3, 4]

for w, players in itertools.product(w_values, num_players):
    print("Testing with w={} and n_players={}".format(w, players))
    for _ in range(TRIALS):
        r_game = random_game(players, a, b)
        print(r_game)
        for k, v in models.items():
            #print(k)
            m = Many(
                {
                    "game": r_game,
                    "w": w,
                    "model_type": v,
                    "initial_victor": 0,
                    "pop_size": 25
                }
            )
            transition_matrix, prediction = m.calculate()
            print("For {} we predict steady state {}".format(k, r(prediction)))
