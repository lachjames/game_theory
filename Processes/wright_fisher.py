from model import Model
import random, math
import numpy as np

# https://www.math.leidenuniv.nl/scripties/CarsouwBach.pdf - seems partially incorrect, re expected time? Or am I misreading it?
# http://www.stats.ox.ac.uk/~didelot/popgen/lecture2.pdf - seems correct
class Wright_Fisher(Model):
    def step(self):
        self.calculate_fitness()

        new_pop = np.zeros_like(self.population)
        for _ in range(np.int(np.sum(self.population))):
            new_pop[self.select()] += 1

        self.population = new_pop

        self.cur_step += 1
