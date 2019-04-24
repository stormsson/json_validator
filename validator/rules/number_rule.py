from validator.rules.base_rule import BaseRule

class NumberRule(BaseRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, value):
        base_validation = super().validate(value)

        is_number = isinstance(value, int) or isinstance(value, float)
        return is_number and base_validation
