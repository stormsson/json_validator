import unittest
import re
from validator.rules.string_rule import StringRule
from validator.rules.regexp_rule import RegexpRule
from validator.schema import Schema

class TestSchemaMixedRule(unittest.TestCase):

    def test_mixed_validation_creates_rules(self):
        s = {
            "key": { "validator": "number|regexp", "parameters": {
                "number":{},
                "regexp":{ "pattern": "test_string" },
            } },
        }

        x = Schema(s)

        self.assertTrue(isinstance(x.rules["key"], list))
        self.assertEqual(2, len(x.rules["key"]))

    def test_mixed_validation_creates_rule_with_empty_validator(self):
        # if the parameters object does not contain the key of the validator
        # a {} object is used
        s = {
            "key": { "validator": "number|regexp", "parameters": {
                # "number":{}, #=> removed
                "regexp":{ "pattern": "test_string" },
            } },
        }

        x = Schema(s)
        self.assertTrue(isinstance(x.rules["key"], list))
        self.assertEqual(2, len(x.rules["key"]))

    def test_isMultipleValidationRule(self):
        s = {
            "key": { "validator": "string|regexp", "parameters": {
                "string":{ "minlength": 10 },
                "regexp":{ "pattern": "test_str" },
                }
            },
            "other_key": { "validator": "number"}
        }
        x = Schema(s)
        self.assertTrue(x._isMultipleValidationRule("key"))
        self.assertFalse(x._isMultipleValidationRule("other_key"))


    def test_mixed_validation(self):
        s = {
            "string_or_regexp_field": { "validator": "string|regexp", "parameters": {
                "string":{ "minlength": 10 },
                "regexp":{ "pattern": "test_str" },
            } },
        }
        x = Schema(s)
        self.assertTrue(x.validate({"string_or_regexp_field":"test_str"}))
        self.assertTrue(x.validate({"string_or_regexp_field":"abcabcabcabc"}))
        self.assertFalse(x.validate({"string_or_regexp_field":"abc"}))

    def test_mixed_validation_just_to_be_safe(self):
        s = {
            "string_or_number_field": { "validator": "string|number", "parameters": {
                "string":{ "minlength": 10 },
                "number":{},
            } },
        }
        x = Schema(s)
        self.assertTrue(x.validate({"string_or_number_field": 4}))
        self.assertTrue(x.validate({"string_or_number_field":"abcabcabcabc"}))
        self.assertFalse(x.validate({"string_or_number_field":"abc"}))


if __name__ == '__main__':
    unittest.main()

