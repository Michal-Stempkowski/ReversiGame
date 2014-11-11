from unittest import TestCase

from ReversiApp.core.human_player import HumanPlayer
from ReversiApp.message_manager import *
from ReversiApp.mocks.core.mock_game_logic import GameInvalidMoveMock, GameValidMoveMock
from ReversiApp.mocks.system_mocks import SystemMessageBusMockWithMessageLog


class WhenPlayingGame(TestCase):
    def setUp(self):
        self.player = HumanPlayer(GameInvalidMoveMock(), SystemMessageBusMockWithMessageLog())

    def test_invalid_move_should_cause_warning(self):
        self.player.make_move(0, 0)
        self.assertEquals([MoveWasNotPossibleMessage()], self.player.message_bus.called)

    def test_valid_move_should_cause_move_done(self):
        self.player.game = GameValidMoveMock()
        self.player.make_move(0, 0)
        self.assertEquals([MoveDoneMessage()], self.player.message_bus.called)

    def test_pass_should_cause_move_passed(self):
        self.player.game = GameValidMoveMock()
        self.player.pass_move()
        self.assertEquals([MovePassedMessage()], self.player.message_bus.called)

    def test_surrender_should_cause_player_surrendered(self):
        self.player.game = GameValidMoveMock()
        self.player.surrender()
        self.assertEquals([PlayerSurrenderedMessage()], self.player.message_bus.called)