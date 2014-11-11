class Message(object):
    def __eq__(self, other):
        return self.__class__ == other.__class__


class MoveWasNotPossibleMessage(Message):
    pass


class MoveDoneMessage(Message):
    pass


class MovePassedMessage(Message):
    pass


class PlayerSurrenderedMessage(Message):
    pass