from unittest import TestCase

from ReversiApp.core.game_logic import Game, GameStateNew, GameStateDead, UnknownGameStateException


class WhenCreatingGame(TestCase):
    def setUp(self):
        self.game = Game()

    def test_game_should_be_in_new_state(self):
        self.assertEquals(GameStateNew(), self.game.get_current_game_state())


class WhenInNewState(TestCase):
    def setUp(self):
        self.game = Game()

    def test_should_raise_exception_on_unregistered_state_change(self):
        with self.assertRaises(UnknownGameStateException):
            self.game.game_state.some_unknown_state()

    def test_should_move_to_dead_state_after_quit_call(self):
        try:
            self.game.game_state.quit(self.game)
        except UnknownGameStateException:
            self.fail("UnknownGameStateException thrown for known method!")

        self.assertEquals(GameStateDead(), self.game.get_current_game_state())