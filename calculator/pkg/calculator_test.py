import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):

    def test_addition_and_multiplication(self):
        calculator = Calculator()
        result = calculator.evaluate("3 + 7 * 2")
        self.assertEqual(result, 17)

if __name__ == '__main__':
    unittest.main()
