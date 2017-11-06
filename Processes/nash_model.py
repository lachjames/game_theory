from model import Model

import nash
import numpy as np

class Nash(Model):
    def find_nash(self):
        g = nash.Game(self.game, np.transpose(self.game))
        return list(g.support_enumeration())