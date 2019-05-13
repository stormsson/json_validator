import unittest
import re
from validator.rules.boolean_rule import BooleanRule

class TestBooleanRule(unittest.TestCase):

    def test_validates_bool(self):
        x = BooleanRule()
        self.assertTrue(x.validate(True))
        self.assertTrue(x.validate(False))


    def test_allow_string_raises_error(self):
        with self.assertRaises(TypeError):
            x = BooleanRule(allow_string="yes")

    #duh
    def test_allow_string_allows_strings(self):
        x = BooleanRule(allow_string=True)
        self.assertTrue(x.validate(True))
        self.assertTrue(x.validate(False))
        self.assertTrue(x.validate("True"))
        self.assertTrue(x.validate("False"))
        self.assertTrue(x.validate("true"))
        self.assertTrue(x.validate("false"))



if __name__ == '__main__':
    unittest.main()

