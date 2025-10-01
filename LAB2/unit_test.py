import unittest
from sum_of_two import sum_of_two

class TestSumOfTwo(unittest.TestCase):

    def test_example1(self):
        self.assertEqual(sum_of_two([2, 7, 11, 15], 9), [0, 1])

    def test_example2(self):
        self.assertEqual(sum_of_two([3, 2, 4], 6), [1, 2])

    def test_example3(self):
        self.assertEqual(sum_of_two([3, 3], 6), [0, 1])

    def test_no_solution(self):
        self.assertEqual(sum_of_two([1, 2, 3], 7), [])

    def test_negative_numbers(self):
        self.assertEqual(sum_of_two([-1, -2, -3, -4], -6), [1, 3])

    def test_with_zero(self):
        self.assertEqual(sum_of_two([0, 4, 3, 0], 0), [0, 3])

    def test_mixed_numbers(self):
        self.assertEqual(sum_of_two([-2, 1, 4, 6], 5), [1, 2])

unittest.main(argv=[''], verbosity=2, exit=False)