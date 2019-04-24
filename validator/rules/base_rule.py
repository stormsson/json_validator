from abc import abstractmethod

class BaseRule():
    def __init__(self):
        self.rules = {}

    @abstractmethod
    def validate(self, value):
        return
