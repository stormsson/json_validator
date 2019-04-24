from validator.rules.base_rule import BaseRule

class StringRule(BaseRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, value):
        base_validation = super().validate(value)

        return isinstance(value, str) and base_validation
