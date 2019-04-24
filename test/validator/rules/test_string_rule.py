import unittest
import re
from validator.rules.string_rule import StringRule

class TestStringRule(unittest.TestCase):

    def test_all(self):
        x = StringRule()
        self.assertTrue(x.validate("ciao"))
        self.assertFalse(x.validate(5))
        self.assertFalse(x.validate({}))
        self.assertFalse(x.validate([]))

    def test_empty_string(self):
        x = StringRule()
        self.assertTrue(x.validate(""))

        x = StringRule(allow_empty=False)
        self.assertFalse(x.validate(""))




if __name__ == '__main__':
    unittest.main()

