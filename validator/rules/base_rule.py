from abc import abstractmethod

class BaseRule():
    def __init__(self, mandatory=False, allow_empty=True, **kwargs):
        self.allow_empty = allow_empty
        self.mandatory=mandatory


    def validate(self, value):
        if not self.allow_empty:
            if (value == None) or (value ==""):
                return False

        return True

