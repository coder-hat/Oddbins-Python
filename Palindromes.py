'''
Ad-hoc code related to palindromes.
'''

def is_palindrome_permutation(s):
    '''
    Determines whether s is a sequence of characters that is permutable into a palindrome.
    This is only true when every character but one in s appears an even number of times.
    returns True if s is a palindrome permutation, False otherwise.
    '''
    letters = set()
    for c in s:
        if c in letters:
            letters.remove(c)
        else:
            letters.add(c)
    return len(letters) < 2

def is_palindrome(s):
    '''
    Determines whether s is a palindromic sequence of characters.
    An s of None, '', or a single characters is a palindrome.
    Sequences of two or more characters are palindromes if nested pairs of characters match.
    The code is case-sensitive. Whitespace and punctuation are treated as part of the sequence.
    E.g. "A rat tara!" is not an palindrome, but "!arattara! is.
    returns True if s is a palindrome, False otherwise.
    '''
    if not s or len(s) < 2:
        return True
    elif s[0] != s[-1:]:
        return False
    else:
        return is_palindrome(s[1:-1])
    return True

def is_palindrome_iter(s):
    while s and len(s) > 1:
        if s[0] == s[-1:]:
            s = s[1:-1]
        else:
            return False
