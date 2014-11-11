class MyMock(object):
    def __init__(self, another_mock=None):
        self.another_mock = another_mock

    def __getattr__(self, item):
        if self.another_mock:
            return self.another_mock.__getattribute__(item)
        else:
            return super().__getattribute__(item)


class InvalidMovementPrognosisMock(MyMock):
    # noinspection PyUnusedLocal
    @staticmethod
    def will_be_valid(*args):
        return False


class GameBoardWithNoValidMovementMock(MyMock):
    # noinspection PyUnusedLocal
    @staticmethod
    def offer_piece(*args):
        return InvalidMovementPrognosisMock()


class GameBoardWithInsertUsageCounterMock(MyMock):
    def __init__(self, another_mock=None):
        super().__init__(another_mock)
        self.insert_usage_counter = 0

    # noinspection PyUnusedLocal
    def insert_piece(self, *args):
        self.insert_usage_counter += 1