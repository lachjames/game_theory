import copy
from unittest import TestCase

from Processes import Moran
from params import Parameters


class TestMoran(TestCase):
    def test_step(self):
        tests = (
            ("w0", Parameters.w0, 0.45, 0.55, 500),
            ("w1", Parameters.w1, 0.45, 0.55, 500),
            ("0alwayswins", Parameters.p1win, 1, 1, 500),
            ("p2invades", Parameters.p2invades, 1, 1, 500)
        )

        for t_name, p, min_found, max_found, num_tests in tests:
            found = [0, 0]
            for _ in range(num_tests):
                t = Moran(copy.deepcopy(p))
                found[t.run_to_extinction()] += 1

            if found[0] < min_found or found[0] > max_found:
                self.fail("Failed test {}: expected between {} and {} successes for type 0, but found {}".format(t_name, min_found, max_found, found[0]))
