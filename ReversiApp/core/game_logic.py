from functools import reduce
from ReversiApp.core.game_board import *


class Game(object):
    def __init__(self):
        self.game_board = None
        self.game_state = GameStateNew()

    def get_current_game_state(self):
        return self.game_state

    def perform_action(self, action):
        action(self)

    def is_in_terminal_state(self):
        return self.game_state.is_terminal()

    def is_in_transient_state(self):
        return self.game_state.is_transient()


class UnreachableGameStateException(Exception):
    pass


class GameState(object):
    def __init__(self, reachable_states):
        self.reachable_states = {x.name() for x in reachable_states}

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __hash__(self):
        return self.name().__hash__()

    @classmethod
    def name(cls):
        return cls.__name__

    def is_state_reachable(self, state):
        return state.name() in self.reachable_states

    def is_terminal(self):
        return len(self.reachable_states) == 0

    def is_transient(self):
        return False

    def announce_winner(self, game_board):
        if not game_board.is_movement_possible(self.get_current_player_color()):
            black, white = game_board.count_pieces(BlackPiece()), game_board.count_pieces(WhitePiece())
            return GameStateBlackVictory() if black > white else (GameStateWhiteVictory() if white > black else NoPiece())


class GameStateNew(GameState):
    def __init__(self):
        super().__init__([GameStateDead, GameStateInitialized])

    def is_transient(self):
        return True


class GameStateDead(GameState):
    def __init__(self):
        super().__init__([])


class GameStateInitialized(GameState):
    def __init__(self):
        super().__init__([GameStateBlackTurn])

    def is_transient(self):
        return True


class GameStateBlackTurn(GameState):
    def __init__(self):
        super().__init__([GameStateWhiteTurn, GameStateWhiteVictory, GameStateBlackVictory, GameStateDraw])

    @staticmethod
    def next_player_state():
        return GameStateWhiteTurn()

    @staticmethod
    def my_victory_state():
        return GameStateBlackVictory()

    @staticmethod
    def get_current_player_color():
        return BlackPiece()


class GameStateWhiteTurn(GameState):
    def __init__(self):
        super().__init__([GameStateBlackTurn, GameStateBlackVictory, GameStateWhiteVictory, GameStateDraw])

    @staticmethod
    def next_player_state():
        return GameStateBlackTurn()

    @staticmethod
    def my_victory_state():
        return GameStateWhiteVictory()

    @staticmethod
    def get_current_player_color():
        return WhitePiece()


class GameStateBlackVictory(GameState):
    def __init__(self):
        super().__init__([])

    @staticmethod
    def enemy_victory_state():
        return GameStateWhiteVictory()

    def is_transient(self):
        return True


class GameStateWhiteVictory(GameState):
    def __init__(self):
        super().__init__([])

    @staticmethod
    def enemy_victory_state():
        return GameStateBlackVictory()

    def is_transient(self):
        return True


class GameStateDraw(GameState):
    def __init__(self):
        super().__init__([])

    def is_transient(self):
        return True


class FutureResult(object):
    def __init__(self):
        self.exists = False
        self._value = None

    def __bool__(self):
        return self.exists

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.exists = True


class Action(object):
    def __init__(self):
        self.result = FutureResult()

    @staticmethod
    def raise_if_state_unreachable(game_logic, state):
        if not game_logic.game_state.is_state_reachable(state):
            raise UnreachableGameStateException


class BlackTurnAction(Action):
    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, GameStateBlackTurn())
        game_logic.game_state = GameStateBlackTurn()


class QuitAction(Action):
    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, GameStateDead())
        game_logic.game_state = GameStateDead()


class InitializeAction(Action):
    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, GameStateInitialized())
        game_logic.game_board = GameBoard()
        game_logic.game_board.add_new_game_starting_pieces()
        game_logic.game_state = GameStateInitialized()


class MakeOwnMovementPrognosisAction(Action):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    def __call__(self, game_logic):
        self.result.value = game_logic.game_board.\
            offer_piece(self.row, self.column, game_logic.get_current_game_state().get_current_player_color())


class MakeEnemyMovementPrognosisAction(MakeOwnMovementPrognosisAction):
    def __call__(self, game_logic):
        self.result.value = game_logic.game_board.\
            offer_piece(self.row, self.column,
                        game_logic.get_current_game_state().get_current_player_color().get_enemy_color())


class MakeMoveAction(Action):
    def __init__(self, movement_prognosis):
        super().__init__()
        self.movement_prognosis = movement_prognosis

    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, game_logic.game_state.next_player_state())
        self.raise_if_state_unreachable(game_logic, game_logic.game_state.my_victory_state())
        self.raise_if_state_unreachable(game_logic, game_logic.game_state.my_victory_state().enemy_victory_state())
        self.raise_if_state_unreachable(game_logic, GameStateDraw())

        self.result.value = self.movement_prognosis.will_be_valid()

        if self.result.value:
            game_logic.game_board = self.movement_prognosis.game_board
            if game_logic.game_board.is_movement_possible(game_logic.game_state.get_current_player_color()):
                game_logic.game_state = game_logic.game_state.next_player_state()
            else:
                game_logic.game_state = game_logic.game_state.announce_winner(game_logic.game_board)


class PassAction(Action):
    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, game_logic.game_state.next_player_state())
        game_logic.game_state = game_logic.game_state.next_player_state()


class SurrenderAction(Action):
    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, game_logic.game_state.my_victory_state().enemy_victory_state())
        game_logic.game_state = game_logic.game_state.my_victory_state().enemy_victory_state()