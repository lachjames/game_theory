from model import Model
import random, math
import numpy as np

# http://www.stats.ox.ac.uk/~didelot/popgen/lecture3.pdf
class Moran(Model):
    def step(self):
        self.calculate_fitness()

        a = self.select()

        proportions = self.population / np.sum(self.population)
        b = np.random.choice(range(len(self.population)), size=1, replace=False, p=proportions)

        self.population[a] += 1
        self.population[b] -= 1

        self.cur_step += 1

    def invasion_probability(self):
        i = self.population[1]
        g = self.gammas()
        print(g)
        s1 = self.sum_prod(i-1, g)
        s2 = self.sum_prod(int(self.n) - 1, g)

        print("S1: ", s1)
        print("S2: ", s2)

        return (1 + s1)/(1 + s2)

    def sum_prod(self, a, g):
        s = 0
        for k in range(1, int(a)): #(1, a-1) really
            p = 1
            for j in range(1, k+1): #(1, k) really
                p *= g[j]
            s += p
        return s

    def gamma_product(self):
        return np.product(self.gammas().keys())

    def gammas(self):
        gammas = {}

        for num_invaders in range(1, int(self.n)):
            num_others = self.n - num_invaders
            f = self._fitness([num_others, num_invaders])

            # The probability that, with x invaders in the population, we will lose an invader
            # - that is, the probability that we choose the non-invader (f[0]) to kill an invader (x / (self.n - 1))
            pr_loss = f[0] * (num_invaders / (self.n - 1))

            # The probability that, with x invaders in the population, we will lose a non-invader
            # - that is, the probability that we choose the invader (f[1]) to kill a non-invader ((n - x) / (self.n - 1))
            pr_gain = f[1] * (num_others / (self.n - 1)) #The probability that, with x invaders in the population, we will lose an invader

            print(f)

            print(pr_loss)
            print(pr_gain)

            gammas[num_invaders] = pr_loss / pr_gain
        return gammas