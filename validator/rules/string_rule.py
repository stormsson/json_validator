from validator.rules.base_rule import BaseRule

class StringRule(BaseRule):
    def __init__(self, minlength=None, maxlength=None, **kwargs):
        super().__init__(**kwargs)
        self.minlength = minlength
        self.maxlength = maxlength

    def validate(self, value):
        base_validation = super().validate(value)


        composite_result = base_validation and isinstance(value, str)

        # if base validation failed or the item is not a string
        # ignore further checks
        if composite_result:
            if self.minlength:
                composite_result = composite_result and (len(value) >= self.minlength)

            if self.maxlength:
                composite_result = composite_result and (len(value) <= self.maxlength)

        return composite_result
