from model import Model
import random, math
import numpy as np

# https://www.math.leidenuniv.nl/scripties/CarsouwBach.pdf - seems partially incorrect, re expected time? Or am I misreading it?
# http://www.stats.ox.ac.uk/~didelot/popgen/lecture2.pdf - seems correct
class Wright_Fisher(Model):
    def step(self):
        new_pop = []
        for _ in range(len(self.population)):
            new_pop = [self.population[self.select()]]
        self.population = new_pop

        self.cur_step += 1
