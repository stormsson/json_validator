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

    def test_force_type_raises_exception_if_unrecognized_type_provided(self):
        with self.assertRaises(TypeError):
            x = NumberRule(force_type="dogs")

    def test_force_type(self):
        x = NumberRule(force_type="int")
        self.assertTrue(x.validate(5))
        self.assertFalse(x.validate(5.4))

        x = NumberRule(force_type="float")
        self.assertFalse(x.validate(5))
        self.assertTrue(x.validate(5.4))


if __name__ == '__main__':
    unittest.main()

