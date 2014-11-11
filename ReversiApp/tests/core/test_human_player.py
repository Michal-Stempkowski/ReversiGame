from unittest import TestCase

from ReversiApp.message_manager import MoveWasNotPossibleMessage
from ReversiApp.mocks.system_mocks import MessageManagerMockWithMessageLog


class HumanPlayer(object):
    def __init__(self, message_manager):
        self.message_manager = message_manager

    def make_move(self, row, column):
        self.message_manager.dispatch_message(MoveWasNotPossibleMessage())


class WhenPlayingGame(TestCase):
    def test_invalid_move_should_cause_warning(self):
        player = HumanPlayer(MessageManagerMockWithMessageLog())
        player.make_move(0, 0)
        self.assertEquals([MoveWasNotPossibleMessage()], player.message_manager.called)