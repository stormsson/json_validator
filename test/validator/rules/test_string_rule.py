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

    def test_minlength(self):
        x = StringRule(minlength=4)
        self.assertFalse(x.validate(""))
        self.assertFalse(x.validate("abc"))
        self.assertTrue(x.validate("abcd"))
        self.assertTrue(x.validate("abcdefg"))

    def test_maxlength(self):
        x = StringRule(maxlength=4)
        self.assertTrue(x.validate(""))
        self.assertTrue(x.validate("abc"))
        self.assertTrue(x.validate("abcd"))
        self.assertFalse(x.validate("abcdefg"))

    def test_minmaxlength(self):
        x = StringRule(minlength=2, maxlength=3)

        self.assertFalse(x.validate("a"))
        self.assertTrue(x.validate("ab"))
        self.assertTrue(x.validate("abc"))
        self.assertFalse(x.validate("abcd"))

    def test_maxlength_with_allow_empty(self):
        x = StringRule(allow_empty=False, maxlength=4)
        self.assertFalse(x.validate(""))




if __name__ == '__main__':
    unittest.main()

