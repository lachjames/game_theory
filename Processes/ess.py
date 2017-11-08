from model import Model
from snash import SNash

import nash
import numpy as np

class ESS(Model):
    def find_ess(self):
        symmetrics = SNash(self.game).find_snash()
        ess = []

        for sym in symmetrics:
            strat = sym[0]
            not_ess = False

            for x in strat:
                if x not in (1.0, 0.0):
                    not_ess = True

                if not_ess:
                    continue

            chosen_strategy = [i for i, l in enumerate(strat) if l == 1.0][0]

            for other_strategy in range(len(self.game)):
                this_game = self.make_game(chosen_strategy, other_strategy)

                # Check if that other strategy has a better payoff vs the chosen strategy than it does with itself
                if this_game[chosen_strategy][chosen_strategy] < this_game[other_strategy][chosen_strategy]:
                    not_ess = True

            if not not_ess:
                ess += [strat]

        return ess

    def make_game(self, i, j):
        return [
            [self.game[i, i], self.game[i, j]],
            [self.game[j, i], self.game[j, j]]
        ]