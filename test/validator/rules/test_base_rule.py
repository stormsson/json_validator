import unittest
import re
from validator.rules.base_rule import BaseRule
from validator.schema import Schema


class TestBaseRule(unittest.TestCase):

    def test_allow_empty(self):
        x = BaseRule(allow_empty=True)
        self.assertTrue(x.validate(""))
        self.assertTrue(x.validate(None))

        x = BaseRule(allow_empty=False)
        self.assertFalse(x.validate(""))
        self.assertFalse(x.validate(None))


    def test_assign_name(self):
        rule_name = "asdfoobar"
        x = BaseRule(name=rule_name)

        self.assertEqual(x.name, rule_name)


    def test_schema_creates_default_parent_references(self):
        s = {
            "key": { "validator": "object", "json_validation_schema":{} },
        }

        x = Schema(s)
        self.assertEqual(x.parent_schema, None)
        self.assertEqual(x, x.rules["key"][0].parent_schema)

    def test_schema_setup_top_schema(self):
        s = {
            "key": { "validator": "object", "json_validation_schema":{} },
        }

        x = Schema(s)

        self.assertEqual(x.top_schema, None)

    def test_schema_get_top_schema(self):
        s = {
            "key": { "validator": "object", "json_validation_schema":{
                "subkey": { "validator": "object", "json_validation_schema":{
                    "subkey_2": { "validator": "object", "json_validation_schema":{} }
                }}
            }},
        }

        x = Schema(s)
        self.assertEqual(x.rules["key"][0].top_schema, x)

        subkey_schema = x.rules["key"][0].rules["subkey"][0]
        self.assertEqual(subkey_schema.top_schema, x)

        subkey2_schema = x.rules["key"][0].rules["subkey"][0].rules["subkey_2"][0]
        self.assertEqual(subkey2_schema.top_schema, x)


if __name__ == '__main__':
    unittest.main()

