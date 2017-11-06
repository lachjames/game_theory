from model import Model

import numpy as np

class Dynamics(Model):
    def __init__(self, game, n):
        self.game = game
        self.n = n
        self.population = np.asarray([n - 1, 1])

        self.cur_step = 1

    def step(self):
        raise NotImplementedError("Called Dynamics.step()")

    def calculate_fitness(self):
        self.fitness = self._fitness(self.population)

        return self.fitness

    def _fitness(self, f_pop, exp=False):
        # Handle overflows here!
        fitness = np.dot(self.game, f_pop) - np.diag(self.game)
        fitness = np.multiply(f_pop, fitness)
        fitness = fitness / np.sum(fitness)

        return fitness

    def _fitness_no_pop_mult(self, f_pop, exp=False):
        fitness = np.dot(self.game, f_pop) - np.diag(self.game)
        fitness = fitness / np.sum(fitness)

        return fitness

    def select(self):
        c = np.random.choice(range(len(self.population)), size=1, replace=False, p=self.fitness)
        # print(c)
        return c

    def run_to_extinction(self):
        while np.count_nonzero(self.population) > 1:
            self.step()
        # print("Done")
        return bool(self.population[1])