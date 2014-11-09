from unittest import TestCase
from ReversiApp.core.game_board import WhitePiece, MovementPrognosis

from ReversiApp.core.game_logic import *


class WhenCreatingGame(TestCase):
    def setUp(self):
        self.game_logic = Game()

    def test_game_should_be_in_new_state(self):
        self.assertEquals(GameStateNew(), self.game_logic.get_current_game_state())

    def test_board_game_should_be_none(self):
        self.assertEquals(None, self.game_logic.game_board)


class WhenInNewState(TestCase):
    def setUp(self):
        self.game_logic = Game()

    def test_should_raise_exception_on_unregistered_state_change(self):
        with self.assertRaises(UnreachableGameStateException):
            self.game_logic.perform_action(BlackTurnAction())

    def test_should_move_to_dead_state_after_quit_call(self):
        self.game_logic.perform_action(QuitAction())
        self.assertEquals(GameStateDead(), self.game_logic.get_current_game_state())

    def test_should_be_able_to_check_if_state_is_reachable(self):
        self.assertTrue(self.game_logic.game_state.is_state_reachable(GameStateDead()))
        self.assertFalse(self.game_logic.game_state.is_state_reachable(GameStateBlackTurn()))

    def test_should_move_to_initialized_state_after_initialize_call(self):
        self.game_logic.perform_action(InitializeAction())
        self.assertEquals(GameStateInitialized(), self.game_logic.get_current_game_state())

    def test_state_repr_should_be_valid(self):
        self.assertEquals('GameStateNew', self.game_logic.game_state.__repr__())


class WhenInInitializedState(TestCase):
    def setUp(self):
        self.game_logic = Game()
        self.game_logic.perform_action(InitializeAction())

    def test_game_board_should_be_ready_to_play(self):
        self.assertNotEquals(None, self.game_logic.game_board)
        self.assertTrue(self.game_logic.game_board.is_ready_for_new_game())

    def test_should_move_to_black_turn_state_after_start_game_call(self):
        self.game_logic.perform_action(BlackTurnAction())
        self.assertEquals(GameStateBlackTurn(), self.game_logic.get_current_game_state())


class InvalidMovementPrognosisMock(object):
    # noinspection PyUnusedLocal
    @staticmethod
    def will_be_valid(*args):
        return False


class GameBoardWithNoValidMovementMock():
    # noinspection PyUnusedLocal
    @staticmethod
    def offer_piece(*args):
        return InvalidMovementPrognosisMock()


class GameStateWhiteTurn(GameState):
    def __init__(self):
        super().__init__([])


class MakeMoveAction(Action):
    def __init__(self, player_color, row, column):
        self.player_color = player_color
        self.row = row
        self.column = column

    def __call__(self, game_logic):
        prognosis = game_logic.game_board.offer_piece(self.row, self.column, self.player_color)

        if prognosis.will_be_valid():
            self.raise_if_state_unreachable(game_logic, GameStateWhiteTurn())


class WhenInBlackTurnState(TestCase):
    def setUp(self):
        self.game_logic = Game()
        self.game_logic.perform_action(InitializeAction())
        self.game_logic.perform_action(BlackTurnAction())

    def test_should_not_be_able_to_make_white_move(self):
        self.game_logic.game_board = GameBoardWithNoValidMovementMock()

        self.game_logic.perform_action(MakeMoveAction(WhitePiece(), 0, 0))
        self.assertEquals(GameStateBlackTurn(), self.game_logic.get_current_game_state())