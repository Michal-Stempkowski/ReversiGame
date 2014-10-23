from unittest import TestCase

from ReversiApp.core.game_logic import Game, GameStateNew, GameStateDead, UnknownGameStateException, \
    GameStateInitialized


class WhenCreatingGame(TestCase):
    def setUp(self):
        self.game_logic = Game()

    def test_game_should_be_in_new_state(self):
        self.assertEquals(GameStateNew(), self.game_logic.get_current_game_state())


class WhenInNewState(TestCase):
    def setUp(self):
        self.game_logic = Game()

    def test_should_raise_exception_on_unregistered_state_change(self):
        with self.assertRaises(UnknownGameStateException):
            self.game_logic.game_state.some_unknown_state()

    def test_should_move_to_dead_state_after_quit_call(self):
        try:
            self.game_logic.game_state.quit(self.game_logic)
        except UnknownGameStateException:
            self.fail("UnknownGameStateException thrown for known method!")

        self.assertEquals(GameStateDead(), self.game_logic.get_current_game_state())

    def test_should_be_able_to_check_if_transition_is_available(self):
        self.assertFalse(self.game_logic.game_state.is_transition_possible('unknown'))
        self.assertTrue(self.game_logic.game_state.is_transition_possible('quit'))

    def test_should_move_to_initialized_state_after_initialize_call(self):
        self.game_logic.game_state.initialize(self.game_logic)
        self.assertEquals(GameStateInitialized(), self.game_logic.get_current_game_state())


class WhenInInitializedState(TestCase):
    def setUp(self):
        self.game_logic = Game()
        self.game_logic.game_state.initialize(self.game_logic)