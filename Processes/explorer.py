from moran import Moran
from wright_fisher import Wright_Fisher
from nash_model import Nash
from snash import SNash

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
                "Run model"
            ]
        )

        if choice == "Load game":
            cur_game = load_game()
        elif choice == "Create game":
            cur_game = create_game()
        elif choice == "Run model":
            run_model()

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
    eligible_models = ["Nash", "Symmetric Nash", "ESS"]
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
    elif selected_model == "Symmetric Nash":
        sn = SNash(cur_game)
        for strat in sn.find_snash():
            print(strat)

if __name__ == "__main__": main()