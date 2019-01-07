import unittest
from LcrEngine import LcrEngine

class TestLcrEngine(unittest.TestCase):

    def test__init__(self):

        expect_players = LcrEngine.MIN_PLAYER_COUNT + 1 # default players value as of 2019-1-07
        lcr = LcrEngine()
        self.assertEqual(lcr.number_of_players, expect_players, 'default number of players')

        expect_players = 7
        lcr = LcrEngine(players=expect_players)
        self.assertEqual(lcr.number_of_players, expect_players, 'valid number of players > default')
    
        with self.assertRaises(RuntimeError):
            lcr = LcrEngine(players=1)

    def testCsvHeaderString(self):
        expect = 'Round,Center,Player0,Player1' # expect when players = 2
        lcr = LcrEngine(players=2)
        self.assertEqual(lcr.csv_header_string(), expect, 'players=2 header')

    def testCsvStateString(self):
        expect = '0,0,3,3,3,3,3' # expect for first call when players = 5
        lcr = LcrEngine(players=5)
        self.assertEqual(lcr.csv_state_string(), expect, 'players=5 initial state')

    def testPlayARound(self):
        lcr = LcrEngine(players=8)
        lcr.set_seed(a=1234)
        lcr.play_a_round()
        expect = '1,3,2,4,2,2,3,2,3,3'
        self.assertEqual(lcr.csv_state_string(), expect, 'state should match expect based on set_seed')


if __name__ == '__main__':
    unittest.main()