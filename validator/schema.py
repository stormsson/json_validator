import json
import importlib
from validator.rules.base_rule import BaseRule
from validator.rules.string_rule import StringRule
from validator.rules.number_rule import NumberRule

class Schema(BaseRule):
    def __init__(self, json_validation_schema, **kwargs):
        super().__init__(**kwargs)

        self.rules = {}
        self.json_validation_schema = json_validation_schema

        self._createValidators(self.json_validation_schema)

    def _translateTypeToClassName(self, typename):
        return typename.title()+"Rule"

    def _translateTypeToModuleName(self, typename):
        return "validator.rules."+typename+"_rule"

    def _createValidator(self, validator_schema):
        t = validator_schema["validator_type"].lower()
        if t == "string":
            return StringRule(**validator_schema)
        elif t == "number":
            return NumberRule(**validator_schema)
        elif t == "object":
            return Schema(validator_schema["schema"], **validator_schema)
        else:
            pass

    def _createValidators(self, schema):

        for key, v in schema.items():
            self.rules[key] = self._createValidator(v)

        # m = self._translateTypeToModuleName(schema["type"])
        # cls_name = self._translateTypeToClassName(schema["type"])

        # v = getattr(importlib.import_module(m), cls_name)

    def validate(self, value):
        base_validation = super().validate(value)
        result = True and base_validation
        for key, v in value.items():
            try:
                result = result and self.rules[key].validate(v)
                print("validating %s: %s result: %s" % (key, v, result))
                if not result:
                    break

            except Exception as e:
                print("validator not found for field %s, ignoring field" % key)

        return result

