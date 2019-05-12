import unittest

from Palindromes import is_palindrome
from Palindromes import is_palindrome_iter
from Palindromes import is_palindrome_permutation


class TestPalindromes(unittest.TestCase):

    test_data = {
        None: True,
        "": True,
        "Q": True,
        "A rat tara!": False,
        "!arattara!": True,
        'tut': True,
        'tuf': False,
        'aa': True,
        'Aa': False,
        'ab': False
    }

    def test_is_palindrome_permutation(self):
        for s, expect in self.test_data.items():
            s = ''.join(sorted(s)) if s else s
            print(s)
            actual = is_palindrome_permutation(s)
            self.assertEqual(actual, expect, "s={0} expect={1} actual={2}".format(s, expect, actual))
    
    def test_is_palindrome(self):
        for s, expect in self.test_data.items():
            actual = is_palindrome(s)
            self.assertEqual(actual, expect, "s={0} expect={1} actual={2}".format(s, expect, actual))

    def test_is_palindrome_iter(self):
        for s, expect in self.test_data.items():
            actual = is_palindrome_iter(s)
            self.assertEqual(actual, expect, "s={0} expect={1} actual={2}".format(s, expect, actual))


if __name__ == '__main__':
    unittest.main()
