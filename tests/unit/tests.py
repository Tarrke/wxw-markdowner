""" Small Unittesting tests """

import unittest

class Tests(unittest.TestCase):
    """ Small Unittesting tests """
    def test_sum(self):
        """Small sum tests"""
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()
