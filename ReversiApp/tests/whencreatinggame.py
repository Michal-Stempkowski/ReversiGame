from unittest import TestCase


class Game(object):
    def get_current_game_state(self):
        return None


class GameStateNew(object):
    pass


class WhenCreatingGame(TestCase):
    def setUp(self):
        self.game = Game()

    def test_game_should_be_in_new_state(self):
        self.assertEquals(GameStateNew(), self.game.get_current_game_state())
        self.assertEquals(True, False)