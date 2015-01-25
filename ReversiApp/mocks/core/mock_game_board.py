from ReversiApp.mocks.core.common_mock import CompositeMock


class InvalidMovementPrognosisMock(CompositeMock):
    # noinspection PyUnusedLocal
    @staticmethod
    def will_be_valid(*args):
        return False


class GameBoardWithNoValidMovementMock(CompositeMock):
    def __init__(self, another_mock=None):
        super().__init__(another_mock)
        self.movement_prognosis_board = None

    # noinspection PyUnusedLocal
    @staticmethod
    def offer_piece(*args):
        return InvalidMovementPrognosisMock()


class ValidMovementPrognosisMock(CompositeMock):
    def __init__(self, game_board, another_mock=None):
        super().__init__(another_mock)
        self.game_board = game_board

    # noinspection PyUnusedLocal
    @staticmethod
    def will_be_valid(*args):
        return True


class GameBoardWithValidMovementMock(CompositeMock):
    def __init__(self, another_mock=None):
        super().__init__(another_mock)
        self.movement_prognosis_board = None

    # noinspection PyUnusedLocal
    @staticmethod
    def offer_piece(*args):
        prognosis = ValidMovementPrognosisMock(GameBoardWithValidMovementMock())
        prognosis.game_board.movement_prognosis_board = prognosis.game_board
        return prognosis

    @staticmethod
    def is_movement_possible(*args):
        return True