class Game(object):
    def __init__(self):
        self.game_state = GameStateNew()

    def get_current_game_state(self):
        return self.game_state


class GameState(object):
    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __getattr__(self, item, *args):
        raise UnknownGameStateException


class GameStateNew(GameState):
    def quit(self, game_logic):
        game_logic.game_state = GameStateDead()


class GameStateDead(GameState):
    pass


class UnknownGameStateException(Exception):
    pass