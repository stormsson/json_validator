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

    def test_get_named_rule_on_self(self):
        validator_name = "test_name"
        s = {
            "key": { "validator": "regexp","pattern":".*", "name":validator_name },
        }

        x = Schema(s)
        r = x._get_named_rule(validator_name)

        self.assertIsNotNone(r)

    def test_get_named_rule_on_top_schema(self):
        validator_name = "test_name"
        s = {
            "named_validator_key": { "validator": "number", "name": validator_name },
            "key": { "validator": "object", "json_validation_schema":{
                "subkey": { "validator": validator_name }
            }},
        }

        x = Schema(s)
        named_validator = x.rules["named_validator_key"][0]

        key_schema = x.rules["key"][0]
        rule = key_schema._get_named_rule(validator_name)

        # from the key schema the named validator from the top schema is retrieved
        self.assertIsNotNone(rule)

        # it is actually the same in the parent named_rules dictionary
        self.assertEqual(rule, named_validator)

        # it has been referenced in the subkey rule
        self.assertEqual(key_schema.rules["subkey"][0], named_validator)



if __name__ == '__main__':
    unittest.main()

