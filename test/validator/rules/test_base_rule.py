import unittest
import re
from validator.rules.base_rule import BaseRule

class TestBaseRule(unittest.TestCase):

    def test_allow_empty(self):
        x = BaseRule(allow_empty=True)
        self.assertTrue(x.validate(""))
        self.assertTrue(x.validate(None))

        x = BaseRule(allow_empty=False)
        self.assertFalse(x.validate(""))
        self.assertFalse(x.validate(None))

if __name__ == '__main__':
    unittest.main()

