import unittest

import GolAR

class TestGolAR(unittest.TestCase):

    # Parts 1 and 2 of "blinker" -- a period 2 oscillator pattern
    # useful as a starting configuration of live-cells
    # http://www.conwaylife.com/ref/lexicon/lex_b.htm#blinker
    #
    # ###
    #
    blinker1 = {(1, 1), (2, 1), (3, 1)}
    #  #
    #  #
    #  #
    blinker2 = {(2, 0), (2, 1), (2, 2)} 

    # acorn is the starting configuration of live-cells
    # Alex R. used as an example in his article.
    #  ##  ###
    #     #
    #   #
    acorn = {(1, 1), (2, 1), (2, 3), (4, 2), (5, 1), (6, 1), (7, 1)}

    def test_conway_rules(self):
        # Input and expected-result data for all valid input values
        expectations = [
            # (is_alive, neighbors, expect)
            (False, 0, False),
            (False, 1, False),
            (False, 2, False),
            (False, 3, True),
            (False, 4, False),
            (False, 5, False),
            (False, 6, False),
            (False, 7, False),
            (False, 8, False),
            (False, 9, False),
            (True, 0, False),
            (True, 1, False),
            (True, 2, True),
            (True, 3, True),
            (True, 4, False),
            (True, 5, False),
            (True, 6, False),
            (True, 7, False),
            (True, 8, False),
            (True, 9, False)
        ]
        for is_alive, neighbors, expect in expectations:
            actual = GolAR.conway_rules(neighbors, is_alive)
            msg = "alive={0} neighbors={1} expect={2} actual={3}".format(is_alive, neighbors, expect, actual)
            self.assertEquals(actual, expect, msg)

    def test_neighbors_rect(self):
        expect = [(1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (0, 0)]
        actual = GolAR.neighbors_rect((1,1))
        self.assertCountEqual(actual, expect)
        # assertCountEqual does more than confirm len(actual) == len(expect):
        # it also confirms that actual and expect contain the same elements
        # although possibly not in the same order.
    
    def test_step(self):
        actual = GolAR.step(GolAR.conway_rules, GolAR.neighbors_rect, TestGolAR.blinker1)
        self.assertCountEqual(actual, TestGolAR.blinker2, "step 1")
        actual = GolAR.step(GolAR.conway_rules, GolAR.neighbors_rect, actual)
        self.assertCountEqual(actual, TestGolAR.blinker1, "step 2")

    def test_life(self):
        gol = GolAR.life(TestGolAR.blinker1)
        self.assertCountEqual(next(gol), TestGolAR.blinker2, "life 1")
        self.assertCountEqual(next(gol), TestGolAR.blinker1, "life 2")
        self.assertCountEqual(next(gol), TestGolAR.blinker2, "life 3")

if __name__ == '__main__':
    unittest.main()