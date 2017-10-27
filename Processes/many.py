import numpy as np

from moran import Moran
from wright_fisher import Wright_Fisher

unit_test_game = np.asarray([
    [3, 3, 2],
    [2, 2, 2],
    [2, 3, 3]
])

def r(x):
    return np.around(x, 3)

def main():
    r_game = random_game(3, 2, 4)
    print(r_game)

    many = Many(
        {
            #"game": np.asarray([
            #    [1, 1, 1],
            #    [1, 1, 1],
            #    [1, 1, 1.01]
            #]),
            "game": r_game,
            #"game": unit_test_game,
            "w": 0.1,
            "model_type": Wright_Fisher,
            "initial_victor": 2,
            "pop_size": 10
        }
    )

    transition_matrix, prediction = many.calculate()

    print("transition matrix:")
    print(np.around(transition_matrix, 3))

    n = 5000

    results, scores = many.run(n / 5, n, 5)
    print(np.around(scores, 3))
    print(results)
    print("Predicted: {}; Actual: {}".format(r(prediction), r(normalize_dict(results))))

def normalize(x):
    s = np.sum(x)
    if s == 0:
        return np.zeros_like(x)
    else:
        norm = np.zeros_like(x)
        for i in range(len(x)):
            # try:
            #     norm[i] = x[i] / s
            # except FloatingPointError as e:
            #     if "underflow" in str(e):
            #         norm[i] = 0
            #         print("Caught underflow with x={}".format(x[i]))
            #     else:
            #         raise e
            norm[i] = x[i] / s
        return norm

def normalize_dict(x):
    l = []
    for key in sorted(x.keys()):
        l += [x[key]]
    return normalize(np.asarray(l, dtype=np.float))

class Many:
    def __init__(self, p):
        self.game = p["game"]
        self.model_type = p["model_type"]
        self.state = p["initial_victor"]
        self.w = p["w"]
        self.pop_size = p["pop_size"]

        self.num_types = len(self.game[0])

    def iterate(self):
        # We will pick a mutation to happen at random
        mutated = np.random.randint(0, self.num_types)

        if mutated == self.state:
            return self.state

        #print("Mutated:", mutated)

        model = self.make_model(self.state, mutated)

        #print(model.population)

        model.run_to_extinction()

        if model.population[0] > 0:
            # We stay in the current state
            pass
        else:
            # The population has mutated
            self.state = mutated
        
        return self.state

    def make_model (self, i, j):
        population = [self.pop_size - 1, 1]

        this_game = [
            [ self.game[i, i], self.game[i, j] ],
            [ self.game[j, i], self.game[j, j] ]
        ]

        #print("The model with (n-1)={} and 1={} has this game:".format(i, j))
        #print(this_game)

        model = self.model_type(
            {
                "game": np.asarray(this_game),
                "w": self.w,
                "init_pop": np.asarray(population)
            }
        )

        return model

    def run(self, start, n, percentages=10):
        wins = {}

        scores = np.zeros_like(self.game, dtype=np.float)

        for x in range(self.num_types):
            wins[x] = 0
        
        for i in range(n):
            if i % (n / percentages) == 0:
                print("{}%".format(i / n * 100))
            before = self.state
            after = self.iterate()
            if i >= start:
                wins[after] += 1
                scores[before, after] += 1
        
        for i in range(self.num_types):
            scores[i,:] = normalize(scores[i,:])

        return wins, scores

    def calculate(self):
        # For each potential sub_game, we calculate the probability of mutation
        transition_matrix = np.asarray([ [0] * self.num_types ] * self.num_types, dtype=np.float)
        
        for i in range(self.num_types):
            for j in range(self.num_types):
                if i == j:
                    transition_matrix[i, j] += 1 / self.num_types
                    continue
                
                model = self.make_model(i, j)
                #print("Invasion probability", model.invasion_probability())

                # try:
                #     pr = model.invasion_probability()
                #     transition_matrix[i, j] = pr / self.num_types
                #     transition_matrix[i, i] += (1 - pr) / self.num_types
                # except FloatingPointError as e:
                #     if "underflow" in str(e):
                #         transition_matrix[i, j] = 0
                #         transition_matrix[i, i] += 1.0 / self.num_types
                #     else:
                #         raise e

                pr = model.invasion_probability()
                transition_matrix[i, j] = pr / self.num_types
                transition_matrix[i, i] += (1 - pr) / self.num_types

        #for i in range(self.num_types):
        #    transition_matrix[i] = normalize(transition_matrix[i])

        w, v = np.linalg.eig(np.transpose(transition_matrix))

        prediction = None

        #We take the eigenvalue closest to 1
        min_eig = float("Inf")
        for i in range(len(w)):
            dist = abs(w[i] - 1)
            if dist < min_eig:
                min_eig = dist
                #print("Average States: ")
                prediction = normalize(v[:,i])
                #print(prediction)
            #print("{} is the eigenvector corresponding to {}".format(v[:,i], w[i]))
            #print("{}")

        return transition_matrix, prediction

def random_game(n, a, b, integer = True):
    g = []
    for _ in range(n):
        r = []
        for _ in range(n):
            if integer:
                r += [np.random.randint(a, b)]
            else:
                r += [np.random.uniform(a, b)]
        g += [r]
    return np.asarray(g)

if __name__ == "__main__": main()