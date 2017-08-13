from moran import Moran
from wright_fisher import Wright_Fisher
import math

num_tests = 100

results = []

freq = [0.5, 0.5]
n = 250
parameters = {
    "n": n,
    "freq": freq,
    # "game": [
    #	[random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)],
    #	[random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)],
    #	[random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)]
    # ],
    "game": [
        [2, 1],
        [1, 1]
    ],
    "w": 1
}

# example_moran = Moran(parameters)
# print("Expected time: " + str(example_moran.expectation()))

wins = {i: 0 for i in range(len(freq))}

for n in range(num_tests):
    if n % 10 == 0:
        print(n)
    moran = Wright_Fisher(parameters=parameters)

    # print("Expected time taken: " + str(moran.expectation()))

    winner = moran.run_to_extinction()
    # print(moran.cur_step)
    # print(winner)
    wins[winner] += 1
    results += [moran.cur_step]

# print(results)
# print(np.average(results))
# print(np.mean(results))

for x in wins:
    wins[x] /= float(num_tests)

print(wins)
