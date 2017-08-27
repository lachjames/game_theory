from moran import Moran
from wright_fisher import Wright_Fisher
import math, random

import numpy as np

num_tests = 1000

# example_moran = Moran(parameters)
# print("Expected time: " + str(example_moran.expectation()))

#tests = ( ("Moran", Moran), ("Wright-Fisher", Wright_Fisher) )
#tests = ( ("Moran", Moran),)

tests = ( ("Wright-Fisher", Wright_Fisher), )

def rand_game(i):
    return np.array(
        [
            [random.randint(-i, i), random.randint(-i, i)],
            [random.randint(-i, i), random.randint(-i, i)]
        ]
    )

for p_name, p in tests:
    results = [0, 0]

    first = True
    game = rand_game(5)
    print

    for n in range(num_tests):
        #game = np.array([[2, 0],[3, 1]], dtype=np.float)
        parameters = {
            "game": game,
            "w": 0.1,
            "init_pop": np.array([3, 1], dtype=np.float)
        }

        if n % 100 == 0:
            print(n)

        t = p(parameters=parameters)

        #t.test_canonical_form()
        #exit()

        if (first and p is Moran):
            first = False
            print("Gamma Product", t.gamma_product())
            print("Fixation Probability", t.invasion_probability())
        if (first and p is Wright_Fisher):
            first = False
            print("Invasion Probability:", t.invasion_probability())
        #exit()
        # print("Expected time taken: " + str(moran.expectation()))

        winner = t.run_to_extinction()
        # print(moran.cur_step)
        # print(winner)

        results[winner] += 1

    print(p_name, "has results:", results)