from model import Model

import nash
import numpy as np

class SNash(Model):
    def find_snash(self):
        g = nash.Game(self.game, np.transpose(self.game))
        eqs = list(g.support_enumeration())

        sym = []

        for eq in eqs:
            if self.symmetric(eq):
                sym += [eq]

        return sym

    def symmetric(self, eq):
        A = eq[0]
        for x in eq:
            if not all(np.isclose(A, x)):
                return False
        return True