from unittest import TestCase
from params import Parameters
from Processes.wright_fisher import Wright_Fisher

import copy

class TestMoran(TestCase):
    def test_step(self):
        tests = (
            ("w0", Parameters.w0, 225, 275, 500),
            ("w1", Parameters.w1, 225, 275, 500),
            ("0alwayswins", Parameters.p1win, 500, 500, 500)
        )

        for t_name, p, min_found, max_found, num_tests in tests:
            found = [0, 0]
            for _ in range(num_tests):
                t = Wright_Fisher(copy.deepcopy(p))
                found[t.run_to_extinction()] += 1

            if found[0] < min_found or found[0] > max_found:
                self.fail("Failed test {}: expected between {} and {} successes for type 0, but found {}".format(t_name, min_found, max_found, found[0]))
