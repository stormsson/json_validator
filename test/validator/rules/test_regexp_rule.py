import unittest
import re
from validator.rules.regexp_rule import RegexpRule

class TestRegexpRule(unittest.TestCase):

    def test_all(self):
        x = RegexpRule(".*")

        self.assertTrue(x.validate(""))
        self.assertTrue(x.validate("ciao"))

    def test_number(self):
        x = RegexpRule("\d+")
        self.assertTrue(x.validate("45"))
        self.assertFalse(x.validate("s"))


    def test_case_insensitive(self):
        x = RegexpRule("ciao", re.IGNORECASE)
        self.assertTrue(x.validate("CIAO"))
        self.assertTrue(x.validate("ciao"))

        x = RegexpRule("ciao")
        self.assertTrue(x.validate("ciao"))
        self.assertFalse(x.validate("CIAO"))



if __name__ == '__main__':
    unittest.main()

