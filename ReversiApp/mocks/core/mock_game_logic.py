from ReversiApp.core.game_logic import FutureResult


class GameInvalidMoveMock(object):
    @staticmethod
    def perform_action(action):
        action.result = FutureResult()


class GameValidMoveMock(object):
    @staticmethod
    def perform_action(action):
        action.result = FutureResult()
        action.result.value = True
