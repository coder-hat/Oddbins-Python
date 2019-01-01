'''
= 2018-12-31 (with minutes to spare!)
LcrEngine contains the rules and data state to play the L-C-R Dice Game.
See: https://en.wikipedia.org/wiki/LCR_(dice_game)

The game is completely based on luck.
It requires no player strategy at all, and is thus simple to automate.
'''

import random

class LcrEngine:

    MIN_PLAYER_COUNT = 2

    def __init__(self, players=3):
        if players < self.MIN_PLAYER_COUNT:
            raise RuntimeError('Cannot init an LcrEngine with < {0} players: players={1}'.format(self.MIN_PLAYER_COUNT, players))
        self.number_of_players = players
        # Each player starts with three tokens
        self.tokens = [int(3) for i in range(self.number_of_players)]
        # Center pot starts with zero tokens
        self.center = int(0)
        # Zero rounds have been played
        # A round has been play after every player has had a turn
        self.round = int(0)
        # Set the faces of a six-sided game die
        self.faces = ['Dot', 'Left', 'Dot', 'Right', 'Dot', 'Center']
        # Configure a dispatcher mapping an action for each possible die face.
        self.roll_action = { 
            'Dot' : self.do_dot, 
            'Left' : self.do_left, 
            'Right' : self.do_right, 
            'Center' : self.do_center 
        }

    def csv_header_string(self):
        hdrlist = ['Round', 'Center']
        hdrlist += ['Player{0}'.format(i) for i in range(self.number_of_players)]
        return ','.join(hdrlist)

    def csv_state_string(self):
        csvlist = [self.round, self.center]
        csvlist += self.tokens
        return ','.join(map(str, csvlist))
        # map() usage above due to clue from Ricardo Reyes, in Stack Overflow item:
        # "How would you make a comma-separated string from a list of strings?"
        # https://stackoverflow.com/questions/44778/how-would-you-make-a-comma-separated-string-from-a-list-of-strings

    def play_a_round(self):
        '''
        One round is completed when every player has taken a turn.
        '''
        for iplayer in range(self.number_of_players):
            self.play_a_turn(iplayer)
        self.round += 1

    def play_a_turn(self, player_index):
        '''
        A player takes a turn by rolling 1 to 3 die, depending on the number of tokens the player has.
        Each die rolled is resolved, and then the player's turn is over.
        A player with zero tokens simply passes their turn -- they may be able to play in future rounds
        if they receive tokens from adjacent players during those player's turns.
        '''
        player_tokens = self.tokens[player_index]
        if player_tokens > 0:
            player_dice = player_tokens if player_tokens < 4 else 3
            for i in range(player_dice):
                self.roll_action[self.roll()](player_index)

    def roll(self):
        return self.faces[random.randrange(len(self.faces))]
    
    def number_of_players_with_tokens(self):
        return sum(1 for player_tokens in self.tokens if player_tokens > 0)

    def game_over(self):
        return self.number_of_players_with_tokens() <= 1

    def do_dot(self, player_index):
        '''Do nothing when a die roll results in a dot.'''
        pass

    def do_left(self, player_index):
        '''
        When a die roll results in a left, transfer one token from player_index
        to the player to the left.
        '''
        player_left = (player_index - 1) % self.number_of_players
        self.tokens[player_left] += 1
        self.tokens[player_index] -= 1
    
    def do_right(self, player_index):
        '''
        When a die roll results in a right, transfer one token from player_index
        to the player to the right.
        '''
        player_right = (player_index + 1) % self.number_of_players
        self.tokens[player_right] += 1
        self.tokens[player_index] -= 1

    def do_center(self, player_index):
        '''
        When a die roll results in a center, transfer one token from player_index
        to the center.
        '''
        self.center += 1
        self.tokens[player_index] -= 1

#----- default main plays a game with 5 players

if __name__ == "__main__":

    lcr = LcrEngine(players=5)
    print(lcr.csv_header_string())
    print(lcr.csv_state_string())

    while not lcr.game_over():
        lcr.play_a_round()
        print(lcr.csv_state_string())
