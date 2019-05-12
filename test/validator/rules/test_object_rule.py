import unittest
import re
from validator.schema import Schema

#Object rule is a Schema instance!
class TestObjectRule(unittest.TestCase):

    def test_all(self):
        x = Schema({})
        self.assertTrue(x.validate({}))
        self.assertFalse(x.validate("string"))

    def test_raises_exception_if_wrong_type_provided(self):
        with self.assertRaises(TypeError):
            x = Schema("string")

if __name__ == '__main__':
    unittest.main()

