import unittest
from validator.schema import Schema

class TestSchema(unittest.TestCase):
    def setUp(self):
        self.wrong_validator_schema = {
            "field": { "validator": "NON_EXISTENT_VALIDATOR" }
        }

        self.missing_param_schema = {
            "field": { "validator": "object" }
        }

        self.missing_param_regexp_schema = {
            "field": { "validator": "regexp" }
        }

        self.base_validators = {
            "string": "StringRule",
            "number": "NumberRule"
        }

    def test_schema_raises_valueerror(self):
        with self.assertRaises(ValueError):
            x = Schema(self.wrong_validator_schema)

    def test_schema_validator_without_schema_param_raise_typeerror(self):
        with self.assertRaises(TypeError):
            x = Schema(self.missing_param_schema)

    def test_regexp_validator_without_pattern_param_raise_typeerror(self):
        with self.assertRaises(TypeError):
            x = Schema(self.missing_param_regexp_schema)

    def test_schema_creates_array_of_rules(self):
        for val_type, val_class in self.base_validators.items():
            s = {
                "key": { "validator": val_type },
            }

            x = Schema(s)
            self.assertTrue(isinstance(x.rules["key"], list))

    def test_schema_creates_rule_for_validator_class(self):
        for val_type, val_class in self.base_validators.items():
            s = {
                "key": { "validator": val_type },
            }

            x = Schema(s)
            self.assertEqual(x.rules["key"][0].__class__.__name__, val_class)

    def test_schema_creates_regexp_rule(self):
        s = {
            "key": { "validator": "regexp","pattern":".*" },
        }

        x = Schema(s)
        self.assertEqual(x.rules["key"][0].__class__.__name__, "RegexpRule")

    def test_schema_creates_object_rule(self):
        s = {
            "key": { "validator": "object", "json_validation_schema":{} },
        }

        x = Schema(s)
        self.assertEqual(x.rules["key"][0].__class__.__name__, "Schema")


if __name__ == '__main__':
    unittest.main()

