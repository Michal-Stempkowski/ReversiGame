class SystemMessageBusMockWithMessageLog(object):
    def __init__(self):
        self.called = []

    def dispatch_message(self, message):
        self.called.append(message)