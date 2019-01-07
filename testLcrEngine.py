import unittest
from LcrEngine import LcrEngine
from LcrEngine import LcrEngineCenterVariant1

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

    def testNumberOfPlayersWithTokens(self):
        # NOTE 2019-1-07
        # This test also *indirectly* exercises number_of_players_with_tokens via game_over method.
        # game_over is used as part of the testing mechanism itself: the whole thing is a bit self-
        # referential and suspect.  Can we do better?
        expect = 11
        lcr = LcrEngine(players=expect)
        lcr.set_seed(a=1234)
        self.assertEqual(lcr.number_of_players_with_tokens(), expect, 'at game start all players have tokens')
        # game over state for set seed should be: '14,32,0,0,0,1,0,0,0,0,0,0,0'
        while not lcr.game_over():
            lcr.play_a_round()
        self.assertEqual(lcr.number_of_players_with_tokens(), 1, 'at game over only 1 player has tokens')

    def testPlayARound(self):
        lcr = LcrEngine(players=8)
        lcr.set_seed(a=1234)
        lcr.play_a_round()
        expect = '1,3,2,4,2,2,3,2,3,3'
        self.assertEqual(lcr.csv_state_string(), expect, 'state should match expect based on set_seed')


class TestLcrEngineCenterVariant1(unittest.TestCase):

    def testPlayARound(self):
        lcr = LcrEngineCenterVariant1(players=8)
        lcr.set_seed(a=1234)
        lcr.play_a_round()
        expect = '1,1,2,4,2,2,5,2,3,3'
        self.assertEqual(lcr.csv_state_string(), expect, 'state should match expect based on set_seed')


if __name__ == '__main__':
    unittest.main()