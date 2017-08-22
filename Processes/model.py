import random, math
import numpy as np

class Model:
    def __init__(self, parameters):
        self.parameters = parameters

        self.game = parameters["game"]
        self.w = parameters["w"]

        self.population = parameters["init_pop"]
        self.n = np.sum(self.population)

        self.cur_step = 1

    def calculate_fitness(self):
        self.fitness = self._fitness(self.population)
        return self.fitness

    def _fitness(self, f_pop):
        if self.w == 0:
            # We don't want to end up with a divide by zero error
            fitness = np.copy(f_pop) / self.n
            return fitness
        fitness = np.dot(self.game, f_pop) - np.diag(self.game)
        fitness = np.multiply(f_pop, fitness)
        fitness = np.exp(self.w * fitness)
        fitness = fitness / np.sum(fitness)

        return fitness

    def select(self):
        c =  np.random.choice(range(len(self.population)), size=1, replace=False, p=self.fitness)
        #print(c)
        return c

    def run_to_extinction(self):
        while np.count_nonzero(self.population) > 1:
            self.step()
        #print("Done")
        return bool(self.population[1])