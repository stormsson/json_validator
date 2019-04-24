import unittest
import re
from validator.rules.number_rule import NumberRule

class TestNumberRule(unittest.TestCase):

    def test_strings_return_false(self):
        x = NumberRule()
        self.assertFalse(x.validate("ciao"))
        self.assertFalse(x.validate("4"))

    def test_struct_return_false(self):
        x = NumberRule()
        self.assertFalse(x.validate({}))
        self.assertFalse(x.validate([]))

    def test_numbers(self):
        x = NumberRule()
        self.assertTrue(x.validate(5))
        self.assertTrue(x.validate(5.4))





if __name__ == '__main__':
    unittest.main()

