from ReversiApp.core.game_logic import Game
from ReversiApp.core.human_player import HumanPlayer


class GameContainer(object):
    @classmethod
    def create(cls, message_bus1, message_bus2):
        game_logic = Game()
        player1 = HumanPlayer(game_logic, message_bus1)
        player2 = HumanPlayer(game_logic, message_bus2)
        return GameContainer(game_logic, player1, player2)

    def __init__(self, game_logic, player1, player2):
        self.game_logic = game_logic
        self.player1 = player1
        self.player2 = player2