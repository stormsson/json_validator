import re
from validator.rules.base_rule import BaseRule

class RegexpRule(BaseRule):
    def __init__(self, pattern, flags=0):
        self.pattern = pattern
        self.re = re.compile(pattern, flags)

    def validate(self, value):
        return self.re.match(value) != None
