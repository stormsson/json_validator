import re
from validator.rules.base_rule import BaseRule
from validator.rules.string_rule import StringRule

class RegexpRule(StringRule):
    def __init__(self, pattern, flags=0, **kwargs):
        self.pattern = pattern
        self.re = re.compile(pattern, flags)

        super().__init__(**kwargs)

    def validate(self, value):
        base_validation = super().validate(value)
        return (self.re.match(value) != None) and base_validation
