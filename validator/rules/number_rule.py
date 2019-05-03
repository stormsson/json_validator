from validator.rules.base_rule import BaseRule

class NumberRule(BaseRule):
    def __init__(self, force_type=None, **kwargs):
        super().__init__(**kwargs)

        if force_type and force_type not in [ "int", "float"]:
            raise TypeError("Unrecognized number type")

        self.force_type = force_type

    def validate(self, value):
        base_validation = super().validate(value)

        is_number = isinstance(value, int) or isinstance(value, float)

        if self.force_type:
            is_number = is_number and (value.__class__.__name__  == self.force_type)

        return is_number and base_validation
