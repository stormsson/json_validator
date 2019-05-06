import unittest
from validator.schema import Schema

class TestSchemaNamedRules(unittest.TestCase):
    def test_schema_default_named_rules(self):
        x = Schema({})
        self.assertEqual(x.named_rules, {})

    def test_schema_creates_named_rule(self):

        validator_name = "test_name"
        s = {
            "key": { "validator": "regexp","pattern":".*", "name":validator_name },
        }

        x = Schema(s)
        named_rules_keys = list(x.named_rules.keys())
        self.assertIn(validator_name, named_rules_keys)
        self.assertEqual(1, len(named_rules_keys))

    def test_named_rule_is_present_among_rules(self):
        validator_name = "test_name"
        s = {
            "key": { "validator": "regexp","pattern":".*", "name":validator_name },
        }

        x = Schema(s)
        rules_keys = list(x.rules.keys())
        self.assertIn("key", rules_keys)
        self.assertEqual(1, len(rules_keys))

    def test_named_rule_is_propagated_to_top_schema(self):
        validator_name = "test_name_2"

        s = {
            "key": { "validator": "object", "json_validation_schema":{
                "subkey": { "validator": "object", "json_validation_schema":{}, "name":validator_name}
            }},
        }

        x = Schema(s)

        #top schema
        named_rules_keys = list(x.named_rules.keys())
        self.assertIn(validator_name, named_rules_keys)
        self.assertEqual(1, len(named_rules_keys))

        #subkey schema
        self.assertEqual(x.rules["key"][0].named_rules, {})



if __name__ == '__main__':
    unittest.main()

