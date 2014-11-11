from ReversiApp.core.game_board import GameBoard


class Game(object):
    def __init__(self):
        self.game_board = None
        self.game_state = GameStateNew()

    def get_current_game_state(self):
        return self.game_state

    def perform_action(self, action):
        action(self)


class UnreachableGameStateException(Exception):
    pass


class GameState(object):
    def __init__(self, reachable_states):
        self.reachable_states = {x.name() for x in reachable_states}

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__class__ is other.__class__

    @classmethod
    def name(cls):
        return cls.__name__

    def is_state_reachable(self, state):
        return state.name() in self.reachable_states


class GameStateNew(GameState):
    def __init__(self):
        super().__init__([GameStateDead, GameStateInitialized])


class GameStateDead(GameState):
    def __init__(self):
        super().__init__([])


class GameStateInitialized(GameState):
    def __init__(self):
        super().__init__([GameStateBlackTurn])


class GameStateBlackTurn(GameState):
    def __init__(self):
        super().__init__([GameStateWhiteTurn])


class GameStateWhiteTurn(GameState):
    def __init__(self):
        super().__init__([])


class Action(object):
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


class MakeWhiteMoveAction(Action):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, GameStateBlackTurn())


class MakeBlackMoveAction(Action):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, GameStateWhiteTurn())
        prognosis = game_logic.game_board.offer_piece()
        if prognosis.will_be_valid():
            game_logic.game_board = prognosis.game_board
            game_logic.game_state = GameStateWhiteTurn()