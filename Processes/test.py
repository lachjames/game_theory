from moran import Moran
from wright_fisher import Wright_Fisher
import math

import numpy as np

num_tests = 100

# example_moran = Moran(parameters)
# print("Expected time: " + str(example_moran.expectation()))

for p_name, p in ( ("Moran", Moran), ("Wright-Fisher", Wright_Fisher) ):
    results = [0, 0]

    first = True

    for n in range(num_tests):
        parameters = {
            "game": np.array([
                [1, 1], # We cooperate and [they cooperate, they defect]
                [1, 1.1]  # We defect and [they cooperate, they defect]
            ], dtype=np.float),
            "w": 0.01,
            "init_pop": np.array([9, 9], dtype=np.float)
        }
        if n % 10 == 0:
            print(n)

        t = p(parameters=parameters)

        if (first and p is Moran):
            first = False
            print("Gamma Product", t.gamma_product())
            print("Fixation Probability", t.invasion_probability())
        #exit()
        # print("Expected time taken: " + str(moran.expectation()))

        winner = t.run_to_extinction()
        # print(moran.cur_step)
        # print(winner)

        results[winner] += 1

    print(p_name, "has results:", results)