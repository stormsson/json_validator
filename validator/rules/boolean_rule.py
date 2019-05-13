from validator.rules.base_rule import BaseRule

class BooleanRule(BaseRule):
    def __init__(self, allow_string=False, **kwargs):
        super().__init__(**kwargs)

        if allow_string and allow_string not in [ True, False]:
            raise TypeError("allow_string parameter only allows boolean values")

        self.allow_string = allow_string

    def validate(self, value):
        base_validation = super().validate(value)


        allowed_values = [ True, False ]

        if self.allow_string:
            allowed_values.append("true")
            allowed_values.append("false")

        if isinstance(value, str):
            value = value.lower()



        return value in allowed_values
