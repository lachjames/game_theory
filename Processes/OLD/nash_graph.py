import nash

from many import Many, random_game, r
from wright_fisher import Wright_Fisher
from moran import Moran

import numpy as np
import matplotlib.pyplot as plt

import itertools

models = {"wf": Wright_Fisher, "moran": Moran}

TRIALS = 10

game_min, game_max = -10, 10

w_values = [0.001, 0.1, 0.5]
pop_sizes = [10, 25, 50]
strategies = range(2, 6)

result_sets = {}

def graph(w, p, strats, g, trials=100):
    matchings = 0

    x = []
    y = []

    for n_strategies in strats:
        y_value = matching_proportion(w, p, n_strategies, trials)
        x += [n_strategies]
        y += [y_value]
    
    g.scatter(x, y)
    g.set_title("w={}, p={}".format(w, p))

def matching_proportion(w, p, strats, trials):
    matches = 0
    for _ in range(trials):
        r_game = random_game(strats, game_min, game_max, integer = False)
        rankings = set()
        for k, v in models.items():
            m = Many(
                {
                    "game": r_game,
                    "w": w,
                    "model_type": v,
                    "initial_victor": np.random.randint(0, strats),
                    "pop_size": p
                }
            )
            transition_matrix, prediction = m.calculate()
            ordered = ordering(prediction)
            rankings.add(tuple(ordered))
        
        if len(rankings) == 1:
            matches += 1
            
    return matches / trials

def ordering(x):
    B = range(len(x))
    return [idx for idx, val in sorted(zip(B, x), key=lambda x: x[1])]

f, axarr = plt.subplots(len(w_values), len(pop_sizes))

for i, w in enumerate(w_values):
    for j, p in enumerate(pop_sizes):
        print("w: {}, p: {}".format(w, p))
        graph(w, p, strategies, axarr[i, j], TRIALS)

plt.show()