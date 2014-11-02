from ReversiApp.core.game_board import GameBoard


class Game(object):
    def __init__(self):
        self.game_board = None
        self.game_state = GameStateNew()

    def get_current_game_state(self):
        return self.game_state


class UnknownGameStateException(Exception):
    pass


class GameState(object):
    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __getattr__(self, item, *args):
        raise UnknownGameStateException

    def is_transition_possible(self, transition):
        return transition in self.__dir__()


class GameStateNew(GameState):
    def quit(self, game_logic):
        game_logic.game_state = GameStateDead()

    def initialize(self, game_logic):
        game_logic.game_board = GameBoard()
        game_logic.game_board.add_new_game_starting_pieces()
        game_logic.game_state = GameStateInitialized()


class GameStateDead(GameState):
    pass


class GameStateInitialized(GameState):
    def start_game(self, game_logic):
        game_logic.game_state = GameStateBlackTurn()


class GameStateBlackTurn(GameState):
    pass