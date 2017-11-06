import numpy as np
import scipy.special
import scipy.stats

import dynamics

binom_dict = {}


# https://www.math.leidenuniv.nl/scripties/CarsouwBach.pdf - seems partially incorrect, re expected time? Or am I misreading it?
# http://www.stats.ox.ac.uk/~didelot/popgen/lecture2.pdf - seems correct
class Wright_Fisher(dynamics.Dynamics):
    def step(self):
        self.calculate_fitness()

        new_pop = np.zeros_like(self.population)
        for _ in range(self.n):
            new_pop[self.select()] += 1

        self.population = new_pop

        self.cur_step += 1

    def test_canonical_form(self):
        T = np.asarray(
            [
                [1, 0, 0, 0, 0],
                [0.5, 0, 0.5, 0, 0],
                [0, 0.5, 0, 0.5, 0],
                [0, 0, 0.5, 0, 0.5],
                [0, 0, 0, 0, 1]
            ]
        )
        return self.canonical_form(T)

    def invasion_probability(self):
        A = self.transition_matrix()
        # print(np.around(A, 3))
        # X = np.copy(A)
        # for i in range(50):
        #    print(i)
        #    X = np.dot(X, A)
        #    print(np.around(X, 3))
        return self.canonical_form(A)["p"]

    def canonical_form(self, A):
        # Calculates the Q component of the canonical form of A

        C = np.copy(A)

        # Swap the 0th and n-1th row
        tmp = np.copy(C[0])
        C[0] = A[self.n - 1]
        C[self.n - 1] = tmp
        # print(np.around(C, 2))

        # Swap the 0tha nd n-1th column
        tmp = np.copy(C[:, 0])
        C[:, 0] = C[:, self.n - 1]
        C[:, self.n - 1] = tmp

        # print("Matrix A in Canonical Form:")
        # print(np.around(C, 2))

        Q = C[0:self.n - 1, 0:self.n - 1]
        R = C[0:self.n - 1, self.n - 1:self.n + 1]

        I = np.identity(self.n - 1)
        N = np.linalg.inv(I - Q)

        B = np.dot(N, R)

        c = np.ones((self.n - 1))
        t = np.dot(N, c)

        p = B[0, 0]

        # print(np.around(Q, 2))
        # print(np.around(R, 2))
        # print(np.around(N, 2))
        # print(np.around(B, 2))

        result = {"Q": Q, "R": R, "C": C, "B": B, "t": t, "p": p}
        # for k, v in result.items():
        #    print(k)
        #    print(np.around(v, 2))

        return result

    def transition_matrix(self):
        # We construct a transition matrix A where A[i, j] is the probability that you will be at j in the (n-1)th step given you're at i in the n-th step.

        f = self.calculate_f("f")
        g = self.calculate_f("g")

        A = np.zeros((self.n + 1, self.n + 1))

        for i in range(0, self.n + 1):
            for j in range(0, self.n + 1):
                A[i, j] = self.P_ij(i, j, f, g)

        # print("Starting canonical form")
        self.canonical_form(A)

        return A

    def calculate_f(self, mode):
        f = []
        for i in range(0, self.n + 1):
            i_pop = np.asarray([i, self.n - i])
            fit = self._fitness_no_pop_mult(i_pop)
            # print(fit)
            if mode == "f":
                f += [fit[0]]
            elif mode == "g":
                f += [fit[1]]
                # print(f)
        return f

    def P_ij(self, i, j, f, g):
        try:
            binom = binom_dict[(self.n, j)]
        except:
            binom = scipy.special.binom(self.n, j)
            binom_dict[(self.n, j)] = binom

        # binom = scipy.special.binom(self.n, j)

        denominator = i * f[i] + (self.n - i) * g[i]
        pr = i * f[i] / denominator

        # if self.n * pr > 10 and self.n * (1 - pr) > 10:
        #     #print("Using normal approximation")
        #     # Normal approximation will be good enough here
        #     mean = self.n * pr
        #     var = self.n * pr * (1 - pr)
        #
        #     return scipy.stats.norm.cdf(j + 0.5, mean, var) - scipy.stats.norm.cdf(j - 0.5, mean, var)

        # b = (self.n - i) * g[i] / denominator

        try:
            # print("B: {}, P: {}, M: {}".format(binom, np.power(pr, j), np.power((1-pr), self.n - j)))
            return binom * np.power(pr, j) * np.power((1 - pr), self.n - j)
        except FloatingPointError as e:
            if "underflow" in str(e):
                return 0
            elif "overflow" in str(e):
                print("ERROR AT: {} with B: {}, P: {}, Q: {}, pr: {}, 1-pr: {}".format(self.n, binom, np.power(pr, j),
                                                                                       np.power((1 - pr), self.n - j),
                                                                                       pr, 1 - pr))
            raise e

        # If pr doesn't work, we can use 1-pr and self.n - j

        # x = scipy.stats.binom.pmf(j, self.n, pr)

        print(x)

        return x