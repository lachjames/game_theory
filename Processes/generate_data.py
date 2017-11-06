from strategies import Many_Strategies, random_game
from wright_fisher import Wright_Fisher
from moran import Moran

import numpy as np

import itertools

import json

import multiprocessing

NUM_CPU = 4

models = {"wf": Wright_Fisher, "moran": Moran}

TESTING = True

game_min, game_max = 1, 10

# Probability of predictions differing (1 - probability that they are the same)
# Probability of the most popular strategy differing

if not TESTING:
    TRIALS = 1000
    pop_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    strategies = range(2, 11) # From 2 to 10 strategies
else:
    TRIALS = 100
    pop_sizes = [10, 20, 30, 40]
    strategies = range(2, 6) # From 2 to 5 strategies

def ordering(x):
    #Orders from least to most likely
    B = range(len(x))
    return [idx for idx, val in sorted(zip(B, x), key=lambda x: x[1])]

def run_test(args):
    print("Working on {}".format(args))
    p, n_strats = args
    results = []
    for _ in range(TRIALS):
        r_game = random_game(n_strats, game_min, game_max, integer=False)
        game_rankings = {x: [] for x in models.keys()}

        for k, v in models.items():
            m = Many_Strategies(
                game = r_game,
                model_type = v,
                initial_victor = np.random.randint(0, n_strats),
                pop_size = p
            )

            transition_matrix, prediction = m.calculate()
            ordered = ordering(prediction)

            game_rankings[k] += tuple(ordered)

        results += [{
            "game": r_game.tolist(),
            "p": p,
            "n_strats": n_strats,
            "rankings": game_rankings
        }]

    print("Done p: {}; n_strats: {}".format(p, n_strats))

    return results

def main():
    p  = multiprocessing.Pool(NUM_CPU)
    all_results = []
    split_results = p.map(run_test, itertools.product(pop_sizes, strategies))
    for x in split_results:
        all_results += x
    #results = list(map(run_test, itertools.product(pop_sizes, strategies)))
    with open("results.json", "w") as f:
        print(json.dumps(all_results), file=f)

if __name__ == "__main__": main()