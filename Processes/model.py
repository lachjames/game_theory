import random, math
import numpy as np
class Model:
    def __init__(self, parameters):
        self.parameters = parameters

        self.n = parameters["n"]
        self.freq = parameters["freq"]
        self.game = parameters["game"]
        self.w = parameters["w"]

        self.population = []

        self.cur_step = 1

        for i, f in enumerate(self.freq):
            count = int(self.n * f)
            self.population += [i] * count

        x = random.shuffle(self.population)

    def select(self):
        payoff_dict = self.payoffs()
        payoff_pop = []

        for x in self.population:
            payoff_pop += [payoff_dict[x]]

        s = sum(payoff_pop)
        for i in range(len(payoff_pop)):
            payoff_pop[i] /= s

        # print(payoff_pop)

        # print([x for x in zip(self.population, payoff_pop)])
        # print(probabilities)

        selected = np.random.choice(range(len(self.population)), 1, p=payoff_pop)[0]

        return selected

    def payoffs(self):
        cur_strategies = set(self.population)
        # print(cur_strategies)
        strat_count = {}
        for strategy in cur_strategies:
            strat_count[strategy] = len([x for x in self.population if x == strategy])

        # print(strat_count)

        payoffs = {}
        for strategy in cur_strategies:
            strategy_payoffs = [(strat_count[j] - (1 if strategy == j else 0)) * self.game[strategy][j] for j in
                                cur_strategies]
            # print("Strategy {} has payoffs {}".format(strategy, strategy_payoffs))
            payoffs[strategy] = sum(strategy_payoffs) / float(len(self.population))

        for x in payoffs:
            payoffs[x] = math.e ** (self.w * payoffs[x])

        # print(self.population)
        # print(payoffs)
        # exit()

        return payoffs

    def run_to_extinction(self):
        while len(set(self.population)) > 1:
            self.step()
        return self.population[0]


num_tests = 100

results = []

freq = [0.3, 0.3, 0.4]
n = 50
parameters = {
    "n": n,
    "freq": freq,
    # "game": [
    #	[random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)],
    #	[random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)],
    #	[random.randint(-100, 100), random.randint(-100, 100), random.randint(-100, 100)]
    # ],
    "game": [
        [2, 1, 0],
        [2, 1, 0],
        [0, 0, 0]
    ],
    "w": 0
}