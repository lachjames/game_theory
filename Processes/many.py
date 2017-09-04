import numpy as np

from moran import Moran
from wright_fisher import Wright_Fisher

def main():
    transition_matrix, prediction = many.calculate()

    print("transition matrix:")
    print(np.around(transition_matrix, 3))

    n = 5000

    results, scores = many.run(n / 5, n, 5)
    print(np.around(scores, 3))
    print(results)
    print("Predicted: {}; Actual: {}".format(prediction, normalize_dict(results)))

def normalize(x):
    return x / sum(x)

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
                    transition_matrix[i, j] = 1
                    continue
                model = self.make_model(i, j)
                #print("Invasion probability", model.invasion_probability())
                transition_matrix[i, j] = model.invasion_probability()

        for i in range(self.num_types):
            transition_matrix[i] = normalize(transition_matrix[i])

        w, v = np.linalg.eig(np.transpose(transition_matrix))

        prediction = None

        for i in range(len(w)):
                if abs(w[i] - 1) < 1e-10:
                    #print("Average States: ")
                    prediction = normalize(v[:,i])
                    #print(prediction)
                #print("{} is the eigenvector corresponding to {}".format(v[:,i], w[i]))
                #print("{}")

        return transition_matrix, prediction

def random_game(n, a, b):
    g = []
    for _ in range(n):
        r = []
        for _ in range(n):
            r += [np.random.randint(a, b)]
        g += [r]
    return np.asarray(g)

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
        "w": 0.1,
        "model_type": Wright_Fisher,
        "initial_victor": 2,
        "pop_size": 10
    }
)

if __name__ == "__main__": main()