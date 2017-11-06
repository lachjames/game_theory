import numpy as np
class Parameters:
    w0 = {
        "game": np.array([
            [1, 1],
            [1, 1]
        ], dtype=np.float),
        "w": 0,
        "init_pop": np.array([100, 100], dtype=np.float)
    }

    w1 = {
        "game": np.array([
            [1, 1],
            [1, 1]
        ], dtype=np.float),
        "w": 1,
        "init_pop": np.array([100, 100], dtype=np.float)
    }

    p1win = {
        "game": np.array([
            [1, 1],
            [0, 0]
        ], dtype=np.float),
        "w": 1,
        "init_pop": np.array([100, 100], dtype=np.float)
    }

    p2invades = {
        "game": np.array([
            [1, 1],
            [2, 2]
        ], dtype=np.float),
        "w": 1,
        "init_pop": np.array([199, 1], dtype=np.float)
    }
