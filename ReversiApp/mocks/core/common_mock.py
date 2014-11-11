class CompositeMock(object):
    def __init__(self, another_mock=None):
        self.another_mock = another_mock

    def __getattr__(self, item):
        if self.another_mock:
            return self.another_mock.__getattribute__(item)
        else:
            return super().__getattribute__(item)