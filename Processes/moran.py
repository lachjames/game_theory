from model import Model
import random, math
import numpy as np

# http://www.stats.ox.ac.uk/~didelot/popgen/lecture3.pdf
class Moran(Model):
    def step(self):
        a = self.select()
        b = a

        # print(a)

        while b == a:
            b = random.randint(0, len(self.population) - 1)

        self.population[b] = self.population[a]
        self.cur_step += 1
