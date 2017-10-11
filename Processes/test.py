from moran import Moran
from wright_fisher import Wright_Fisher
import math, random

from moran_old import Moran_OLD

import numpy as np

num_tests = 1000

# example_moran = Moran(parameters)
# print("Expected time: " + str(example_moran.expectation()))

tests = ( ("Moran", Moran), ("Wright-Fisher", Wright_Fisher) )
#tests = ( ("Moran", Moran),)

#tests = ( ("Wright-Fisher", Wright_Fisher), )

#tests = ( ("Moran", Moran), ("Moran_OLD", Moran_OLD))

def rand_game(i):
    return np.array(
        [
            [random.randint(-i, i), random.randint(-i, i)],
            [random.randint(-i, i), random.randint(-i, i)]
        ]
    )

#game = rand_game(5)
game = np.array(
    [
        [1, 1],
        [4, -2]
    ]
)

for p_name, p in tests:
    results = [0, 0]

    first = True

    for n in range(num_tests):
        #game = np.array([[2, 0],[3, 1]], dtype=np.float)
        parameters = {
            "game": game,
            "w": 0.1,
            "init_pop": np.array([9, 1], dtype=np.float)
        }

        if n % 100 == 0:
            print(n)

        t = p(parameters=parameters)

        #t.test_canonical_form()
        #exit()

        if (first and p is Moran):
            #print("Gamma Product", t.gamma_product())
            print("Invasion Probability", t.invasion_probability())
        if (first and p is Wright_Fisher):
            print("Invasion Probability:", t.invasion_probability())
        if (first and p is Moran_OLD):
            #print("Gamma Product", t.gamma_product())
            print("Invasion Probability", t.invasion_probability())

        first = False
        #exit()
        # print("Expected time taken: " + str(moran.expectation()))

        winner = t.run_to_extinction()
        #print(moran.cur_step)
        #print(winner)

        results[winner] += 1

    print(p_name, "has results:", results)