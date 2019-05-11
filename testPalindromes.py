import unittest

from Palindromes import is_palindrome


class TestPalindromes(unittest.TestCase):
    def test_is_palindrome(self):
        self.assertTrue(is_palindrome(None), "s is None")
        self.assertTrue(is_palindrome("a"), "s is single letter")

        test_data = {
            "A rat tara!": False,
            "!arattara!": True,
            'tut': True,
            'tuf': False,
            'aa': True,
            'ab': False
        }
        for s in test_data:
            expect = test_data[s]
            actual = is_palindrome(s)
            self.assertEqual(actual, expect, "s={0} expect={1} actual={2}".format(s, expect, actual))

if __name__ == '__main__':
    unittest.main()
