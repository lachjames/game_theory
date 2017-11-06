from moran import Moran
from wright_fisher import Wright_Fisher
import math, random

from moran_old import Moran_OLD

from many import Many, r

import numpy as np

import nash

NUM_TESTS = 1

# example_moran = Moran(parameters)
# print("Expected time: " + str(example_moran.expectation()))

tests = ( ("Moran", Moran), ("Wright-Fisher", Wright_Fisher) )
#tests = ( ("Moran", Moran),)

#tests = ( ("Wright-Fisher", Wright_Fisher), )

#tests = ( ("Moran", Moran), ("Moran_OLD", Moran_OLD))

#game = np.asarray([[-1, 5], [1, 0]])
#game = np.asarray([[2, -4], [4, 0]])
game = np.asarray([ [2, 1], [4, -2] ])

def nearest(X, vectors):
    closest_vector = None
    min_distance = None

    for v in vectors:
        dist = np.linalg.norm(X - v[0])
        if min_distance is None or dist < min_distance:
            min_distance = dist
            closest_vector = v

    return closest_vector

def rand_game(i):
    return np.array(
        [
            [random.randint(-i, i), random.randint(-i, i)],
            [random.randint(-i, i), random.randint(-i, i)]
        ]
    )


for _ in range(NUM_TESTS):
    #game = rand_game(5)

    n = nash.Game(game, np.transpose(game))

    print(n)

    equilibria = [np.asarray(x) for x in n.support_enumeration()]
    
    print("Equilibria:")
    for x in equilibria:
        print(x)

    for p_name, p in tests:
        #game = np.array([[2, 0],[3, 1]], dtype=np.float)
        parameters = {
            "game": game,
            "w": 0.1,
            "model_type": p,
            "pop_size": 100,
            "initial_victor": 0,
        }

        m = Many(parameters)

        transition_matrix, prediction = m.calculate()


        closest = nearest(prediction, equilibria)

        print("For {}, its steady state {} is closest to NE {}".format(p_name, r(prediction), r(closest)))