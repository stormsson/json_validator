import json
import importlib
from validator.rules.base_rule import BaseRule
from validator.rules.string_rule import StringRule
from validator.rules.number_rule import NumberRule
from validator.rules.regexp_rule import RegexpRule

class Schema(BaseRule):
    def __init__(self, json_validation_schema, **kwargs):
        super().__init__(**kwargs)

        self.rules = {}
        self.named_rules = {}

        self.json_validation_schema = json_validation_schema

        self._createValidators(self.json_validation_schema)


    def _createValidator(self, validator_schema):
        t = validator_schema["validator"].lower()
        validators = []

        multiple_validation = False

        # create an array of different validators types
        # if the validator field is in format xyz|abc|...
        if "|" in t:
            split_validators = t.split("|")
            multiple_validation = True
        else:
            split_validators = [ t ]

        # foreach validator type
        for t in split_validators:

            # try to check if there is a 'parameters' parameter in the validator_schema:
            # if present, each key inside this parameter will contain the parameters for the specific validator
            # if not present, then the 'validator_schema' is the parameters array

            if multiple_validation:
                # for each validator check the 'parameters' dictionary for its parameter
                # if no key is found, an empty dictionary is used.
                # some validator require mandatory parameters, not passing them will cause a TypeError
                try:
                    parameters = validator_schema["parameters"][t]
                except Exception as e:
                    parameters = {}
            else:
                parameters = validator_schema

            if t == "string":
                validator = StringRule(**parameters, parent=self)
            elif t == "number":
                validator = NumberRule(**parameters, parent=self)
            elif t == "regexp":
                validator = RegexpRule(**parameters, parent=self)
            elif t == "object":
                validator = Schema(**parameters, parent=self)
            else:
                raise ValueError("Unknown validator type: %s" % t)

            ## add the validator to the named_rules validator
            if validator.name is not None:
                top = self._get_top_schema()
                if top:
                    top.named_rules[validator.name] = validator
                else:
                    self.named_rules[validator.name] = validator

            validators.append(validator)

        return validators

    def _isMultipleValidationRule(self, key):
        return len(self.rules[key]) > 1

    def _createValidators(self, schema):

        for key, v in schema.items():
            self.rules[key] = self._createValidator(v)

        # m = self._translateTypeToModuleName(schema["type"])
        # cls_name = self._translateTypeToClassName(schema["type"])

        # v = getattr(importlib.import_module(m), cls_name)



    def validate(self, value):
        base_validation = super().validate(value)
        result = True and base_validation
        # apply rules validation only if base validation didn't already fail
        if result:
            for key, v in value.items():
                # if multiple validation is used, only one of the validators
                # needs to be True in order to validate positively
                if self._isMultipleValidationRule(key):
                    # we ignore base_validation, which is already ok because we entered the loop
                    result = False
                    try:
                        for key_validator in self.rules[key]:
                            result = result or key_validator.validate(v)
                            # print("checking '%s' field. result: %s. validator used: %s " % (key, result, type(key_validator)))
                    except KeyError as e:
                        print("validator not found for field %s (multiple), ignoring field" % key)
                else:
                    try:
                        for key_validator in self.rules[key]:
                            result = result and key_validator.validate(v)
                            if not result:
                                break
                    except KeyError as e:
                        print("validator not found for field %s, ignoring field" % key)

        return result

