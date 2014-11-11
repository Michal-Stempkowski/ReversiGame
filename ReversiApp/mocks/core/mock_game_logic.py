class GameInvalidMoveMock(object):
    @staticmethod
    def perform_action(action):
        action.result = False


class GameValidMoveMock(object):
    @staticmethod
    def perform_action(action):
        action.result = True
