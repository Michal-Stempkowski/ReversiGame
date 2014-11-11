from ReversiApp.core.game_logic import *
from ReversiApp.message_manager import *


class HumanPlayer(object):
    def __init__(self, game, message_manager):
        self.message_bus = message_manager
        self.game = game

    def make_move(self, row, column):
        prognosis = self.game.perform_action(MakeOwnMovementPrognosisAction(row, column))
        action = MakeMoveAction(prognosis)
        self.game.perform_action(action)

        message = MoveDoneMessage() if action.result else MoveWasNotPossibleMessage()
        self.message_bus.dispatch_message(message)

    def pass_move(self):
        self.game.perform_action(PassAction())
        self.message_bus.dispatch_message(MovePassedMessage())

    def surrender(self):
        self.game.perform_action(SurrenderAction())
        self.message_bus.dispatch_message(PlayerSurrenderedMessage())