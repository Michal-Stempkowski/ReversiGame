from ReversiApp.core.game_board import GameBoard, BlackPiece, WhitePiece


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

    @staticmethod
    def next_player_state():
        return GameStateWhiteTurn()


class GameStateWhiteTurn(GameState):
    def __init__(self):
        super().__init__([GameStateBlackTurn])

    @staticmethod
    def next_player_state():
        return GameStateBlackTurn()


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


class MakeWhiteMovementPrognosisAction(Action):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    def __call__(self, game_logic):
        self.result.value = game_logic.game_board.offer_piece(self.row, self.column, WhitePiece())


class MakeBlackMovementPrognosisAction(Action):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column

    def __call__(self, game_logic):
        self.result.value = game_logic.game_board.offer_piece(self.row, self.column, BlackPiece())


class MakeMoveAction(Action):
    def __init__(self, movement_prognosis):
        super().__init__()
        self.movement_prognosis = movement_prognosis

    def __call__(self, game_logic):
        self.raise_if_state_unreachable(game_logic, game_logic.game_state.next_player_state())
        self.result.value = self.movement_prognosis.will_be_valid()

        if self.result.value:
            game_logic.game_board = self.movement_prognosis.game_board
            game_logic.game_state = game_logic.game_state.next_player_state()


class PassAction(Action):
    def __call__(self, game_logic):
        game_logic.game_state = game_logic.game_state.next_player_state()