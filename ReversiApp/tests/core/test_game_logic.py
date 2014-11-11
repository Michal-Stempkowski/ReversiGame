from unittest import TestCase

from ReversiApp.core.game_logic import *
from ReversiApp.mocks.core.mock_game_board import *


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


class WhenInBlackOrWhiteTurnState(TestCase):
    def setUp(self):
        self.game_logic = Game()
        self.game_logic.game_board = GameBoardWithValidMovementMock()
        self.game_logic.perform_action(InitializeAction())
        self.game_logic.perform_action(BlackTurnAction())

    def assert_movement_prognosis_result(self, game_board, action, is_valid):
        self.game_logic.game_board = game_board
        self.assertFalse(action.result)
        self.game_logic.perform_action(action)
        self.assertTrue(action.result)
        self.assertEquals(is_valid, action.result.value.will_be_valid())

    def assert_should_be_able_to_make_movement_prognosis(self, current_state):
        self.game_logic.game_state = current_state
        self.assert_movement_prognosis_result(
            GameBoardWithNoValidMovementMock(),
            MakeBlackMovementPrognosisAction(0, 0),
            False)
        self.assert_movement_prognosis_result(
            GameBoardWithValidMovementMock(),
            MakeBlackMovementPrognosisAction(0, 0),
            True)
        self.assert_movement_prognosis_result(
            GameBoardWithNoValidMovementMock(),
            MakeWhiteMovementPrognosisAction(0, 0),
            False)
        self.assert_movement_prognosis_result(
            GameBoardWithValidMovementMock(),
            MakeWhiteMovementPrognosisAction(0, 0),
            True)

    def test_should_be_able_to_make_movement_prognosis(self):
        self.assert_should_be_able_to_make_movement_prognosis(GameStateBlackTurn())
        self.assert_should_be_able_to_make_movement_prognosis(GameStateWhiteTurn())

    def assert_movement_result(self, game_board, game_board_changed_assertion, movement_made_assertion,
                               state_after_action):
        self.game_logic.game_board = game_board
        self.assertIsNot(self.game_logic.game_board, self.game_logic.game_board.movement_prognosis_board)
        action = MakeMoveAction(self.game_logic.game_board.offer_piece())
        self.game_logic.perform_action(action)
        game_board_changed_assertion(self.game_logic.game_board, self.game_logic.game_board.movement_prognosis_board)
        self.assertEquals(state_after_action, self.game_logic.get_current_game_state())
        self.assertTrue(action.result)
        self.assertNotEqual(None, action.result.value)
        movement_made_assertion(action.result.value)

    def assert_should_be_able_to_make_only_valid_movement(self, current_state, next_state):
        self.game_logic.game_state = current_state
        self.assert_movement_result(GameBoardWithNoValidMovementMock(), self.assertIsNot, self.assertFalse,
                                    current_state)
        self.assert_movement_result(GameBoardWithValidMovementMock(), self.assertIs, self.assertTrue,
                                    next_state)

    def test_should_be_able_to_make_only_valid_movement(self):
        self.assert_should_be_able_to_make_only_valid_movement(GameStateBlackTurn(), GameStateWhiteTurn())
        self.assert_should_be_able_to_make_only_valid_movement(GameStateWhiteTurn(), GameStateBlackTurn())

    def assert_next_state_after_pass(self, current_state, next_state):
        self.game_logic.game_state = current_state
        self.game_logic.perform_action(PassAction())
        self.assertEquals(next_state, self.game_logic.get_current_game_state())

    def test_should_be_able_to_pass_turn(self):
        self.assert_next_state_after_pass(GameStateBlackTurn(), GameStateWhiteTurn())
        self.assert_next_state_after_pass(GameStateWhiteTurn(), GameStateBlackTurn())

    def assert_on_surrender_state_is(self, current_player, winner):
        self.game_logic.game_state = current_player
        self.game_logic.perform_action(SurrenderAction())
        self.assertEquals(winner, self.game_logic.get_current_game_state())

    def test_should_be_able_to_surrender(self):
        self.assert_on_surrender_state_is(GameStateBlackTurn(), GameStateWhiteVictory())
        self.assert_on_surrender_state_is(GameStateWhiteTurn(), GameStateBlackVictory())