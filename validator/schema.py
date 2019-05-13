import json
import importlib
from validator.rules.base_rule import BaseRule
from validator.rules.string_rule import StringRule
from validator.rules.number_rule import NumberRule
from validator.rules.boolean_rule import BooleanRule
from validator.rules.regexp_rule import RegexpRule

class Schema(BaseRule):
    def __init__(self, json_validation_schema, **kwargs):
        super().__init__(**kwargs)

        if not isinstance(json_validation_schema, dict):
            raise TypeError("Schema or Object Validator must have a dictionary as parameter")

        self.rules = {}
        self.named_rules = {}
        self.mandatory_fields = []

        self.json_validation_schema = json_validation_schema

        self._createValidators(self.json_validation_schema)


    def _get_named_rule(self, name):
        ts = self._get_top_schema()

        if not ts:
            ts = self

        try:
            named_rule = ts.named_rules[name]
        except Exception as e:
            named_rule = None

        return named_rule


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

            # if a named rule with the same namealready exists,
            # it has the precedence over everything else

            named_rule = self._get_named_rule(t)
            if named_rule:
                validator = named_rule
            else:

                # try to check if there is a 'parameters' parameter in the validator_schema:
                # if present, each key inside this parameter will contain the parameters for the specific validator
                # when a multiple validation is requested.
                # If not present, then the whole 'validator_schema' already is the parameters array

                if multiple_validation:
                    # Check the 'parameters' dictionary for the validator parameter
                    # if no key is found, an empty dictionary is used.
                    # Some validator require mandatory parameters, not passing them will cause a TypeError
                    try:
                        parameters = validator_schema["parameters"][t]
                    except Exception as e:
                        parameters = {}

                    # A multiple validation is occurring, a parameter array is present
                    # the parameter dictionary is the definition of a validator
                    if ("validator" in parameters) :
                        t = parameters["validator"]

                else:
                    parameters = validator_schema

                if t == "string":
                    validator = StringRule(**parameters, parent=self)
                elif t == "boolean":
                    validator = BooleanRule(**parameters, parent=self)
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

            # check mandatory requirement on validator
            for r in self.rules[key]:
                if r.mandatory == True:
                    self.mandatory_fields.append(key)
                    break


        # m = self._translateTypeToModuleName(schema["type"])
        # cls_name = self._translateTypeToClassName(schema["type"])

        # v = getattr(importlib.import_module(m), cls_name)


    def _checkMandatoryFieldsArePresent(self, json_data):

        try:
            all_fields = json_data.keys()

        except Exception as e:
            print(json_data)
            return True

        for field in self.mandatory_fields:
            if field not in all_fields:
                return False
        return True

    def validate(self, json_data):
        base_validation = super().validate(json_data)

        # if json_data is not a dictionary we stop everything
        result = True and base_validation and isinstance(json_data, dict)

        # check mandatory field presence
        result = result and self._checkMandatoryFieldsArePresent(json_data)

        # apply rules validation only if base validation didn't already fail
        if result:
            for key, v in json_data.items():
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

