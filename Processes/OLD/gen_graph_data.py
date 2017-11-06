from many import Many, random_game, r
from wright_fisher import Wright_Fisher
from moran import Moran

import numpy as np

import itertools

import json

import multiprocessing

NUM_CPU = 4

models = {"wf": Wright_Fisher, "moran": Moran}

TRIALS = 100

TESTING = True

game_min, game_max = 1, 10

# Probability of predictions differing (1 - probability that they are the same)
# Probability of the most popular strategy differing

if not TESTING:
    #w_values = [0.001, 0.01, 0.1, 1]
    w_values = [1]
    pop_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    strategies = range(2, 11) # From 2 to 10 strategies
else:
    #w_values = [0.1, 0.5, 1]
    w_values = [1]
    #pop_sizes = [10, 20, 50, 100]
    #strategies = range(2, 6) # From 2 to 10 strategies
    pop_sizes = [10, 100]
    strategies = range(2, 5) # From 2 to 10 strategies
# Functional distance - do some reading about ways to measure distance between probability distributions
# Do a similar plot with the distance between the predictions, maybe the average distance?
# For a given p, w, s find the average distance between the two probability distributions
# How many samples are we taking

# Maybe try 1000 samples?

# Find a "good example": Find one game that is simple, s.t. the distance is large

# What's happening in the game [ [1, 1], [4, -2] ]?

# Create a "zoo" and examine it under a microscope

def ordering(x):
    #Orders from least to most likely
    B = range(len(x))
    return [idx for idx, val in sorted(zip(B, x), key=lambda x: x[1])]

def run_test(args):
    print("Working on {}".format(args))
    w, p, n_strats = args
    results = []
    for _ in range(TRIALS):
        r_game = random_game(n_strats, game_min, game_max, integer=False)
        game_rankings = {x: [] for x in models.keys()}

        for k, v in models.items():
            m = Many(
                {
                    "game": r_game,
                    "w": w,
                    "model_type": v,
                    "initial_victor": np.random.randint(0, n_strats),
                    "pop_size": p
                }
            )

            transition_matrix, prediction = m.calculate()
            ordered = ordering(prediction)

            game_rankings[k] += tuple(ordered)

        results += [{
            "game": r_game.tolist(),
            "w": w,
            "p": p,
            "n_strats": n_strats,
            "rankings": game_rankings
        }]

    print("Done w: {}; p: {}; n_strats: {}".format(w, p, n_strats))

    return results

def main():
    p  = multiprocessing.Pool(NUM_CPU)
    all_results = []
    split_results = p.map(run_test, itertools.product(w_values, pop_sizes, strategies))
    for x in split_results:
        all_results += x
    # results = list(map(run_test, itertools.product(w_values, pop_sizes, strategies)))
    with open("results.json", "w") as f:
        print(json.dumps(all_results), file=f)

if __name__ == "__main__": main()