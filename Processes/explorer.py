from moran import Moran
from wright_fisher import Wright_Fisher
from nash_model import Nash
from snash import SNash
from ess import ESS
from strategies import Many_Strategies, random_game, r

import numpy as np

affirmative = ["y", "yes"]

models = {
    "Wright-Fisher": Wright_Fisher,
    "Moran": Moran,
    #"Mixed Nash": Nash,
    #"Symmetric Mixed Nash": SNash,
    #"ESS": ESS
}

cur_game = []

def spacer(n = 24):
    print("_" * n)

def main():
    global cur_game

    while True:
        # Input loop

        # Current game
        spacer()
        print("Current game")
        print_game(cur_game)
        spacer()

        # Get choice
        choice = select_option(
            "Choose an option",
            [
                "Load game",
                "Create game",
                "Random game",
                "Run model",
                "Compute for game"
            ]
        )

        if choice == "Load game":
            cur_game = load_game()
        elif choice == "Create game":
            cur_game = create_game()
        elif choice == "Random game":
            cur_game = gen_random_game()
        elif choice == "Run model":
            run_model()
        elif choice == "Compute for game":
            compute_game()

def select_option(msg, options):
    print(msg)

    for i, x in enumerate(options):
        print("{}: {}".format(i, x))

    return options[get_int("Choice (0-{})".format(len(options) - 1))]

def get_bool(msg):
    return True if input(msg + ": ") in affirmative else False

def get_int(msg):
    return int(input(msg + ": "))

def get_list(msg, f = get_int, n = None):
    the_list = []
    print("List {} = {}".format(msg, the_list))
    while get_bool("Add an element" ):
        print("List {} = {}".format(msg, the_list))
        the_list += [f("Element")]
    return the_list

def load_game():
    games = {
        "Prisoners Dilemma": np.asarray(
            [
                [1, 5],
                [0, 3]
            ]
        )
    }
    selected_game = select_option("Select a game", list(games.keys()))

    return games[selected_game]

def create_game():
    n_strats = get_int("Number of strategies")

    game = [ [0 for x in range(n_strats)] for x in range(n_strats) ]

    for x in range(n_strats):
        for y in range(n_strats):
            print_game(game)
            game[x][y] = get_int("({}, {})".format(x, y))

    return np.asarray(game)

def print_game(game):
    for x in game:
        for y in x:
            print(y, end=" ")
        print()

def run_model():
    eligible_models = ["Nash", "Symmetric Nash", "ESS", "Many"]
    if len(cur_game) == 2:
        eligible_models += ["Moran", "Wright Fisher"]

    selected_model = select_option("Select a model", eligible_models)

    if selected_model == "Moran":
        m = Moran(cur_game, get_int("Population size"))
        print("Invasion probability: {}%".format(m.invasion_probability() * 100))
    elif selected_model == "Wright Fisher":
        wf = Wright_Fisher(cur_game, get_int("Population size"))
        print("Invasion probability: {}%".format(wf.invasion_probability() * 100))
    elif selected_model == "Nash":
        n = Nash(cur_game)
        for strat in n.find_nash():
            print(strat)
    elif selected_model == "Many":
        selected_type = select_option("Select a model type", ["Moran", "Wright Fisher"])
        population_size = get_int("Population size")
        if selected_type == "Moran":
            m = Moran
        elif selected_type == "Wright Fisher":
            m = Wright_Fisher
        many_model = Many_Strategies(cur_game, m, 0, population_size)
        transition_matrix, prediction = many_model.calculate()
        print("Transition matrix:")
        print(transition_matrix)
        print("Prediction:")
        print(prediction)

    elif selected_model == "Symmetric Nash":
        sn = SNash(cur_game)
        for strat in sn.find_snash():
            print(strat)
    elif selected_model == "ESS":
        ess = ESS(cur_game)
        for strat in ess.find_ess():
            print("ESS: " + str(strat))

def compute_game(game = None, pop_size = None, atol = 0.001):
    if game is None:
        game = cur_game

    if pop_size is None:
        pop_size = get_int("Population size")

    wf_model = Many_Strategies(game, Wright_Fisher, 0, pop_size)
    wf_tm, wf_pred = wf_model.calculate()

    moran_model = Many_Strategies(game, Moran, 0, pop_size)
    moran_tm, moran_pred = moran_model.calculate()

    sym_nash = SNash(game)
    nash = sym_nash.find_snash()

    moran_match = None
    wf_match = None

    for n in nash:
        print("Symmetric Nash Equilibrium: {}".format(n[0]))
        if all(np.isclose(moran_pred, n[0], atol=atol)):
            moran_match = n[0]
        if all(np.isclose(wf_pred, n[0], atol=atol)):
            wf_match = n[0]

    if moran_match is None:
        print("Moran did not match with a Nash equilibria, with p={}".format(r(moran_pred)))
    else:
        print("Moran matched with Nash equilibria {}".format(moran_match))

    if wf_match is None:
        print("WF did not match with a Nash equilibria, with p={}".format(r(wf_pred)))
    else:
        print("WF matched with Nash equilibria {}".format(wf_match))

def gen_random_game():
    num_strats = get_int("Number of strategies")
    min_x = get_int("Min value")
    max_x = get_int("Max value")
    return random_game(num_strats, min_x, max_x)


if __name__ == "__main__": main()