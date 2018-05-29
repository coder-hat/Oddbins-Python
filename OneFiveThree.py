
# Non-recursive implementation of integer_to_digits method.
#
##def integer_to_digits(i):
##    """Return a list of the digits of the specified integer.
##    e.g. integer_to_digits(123) returns [1, 2, 3]"""
##    digits = []
##    while i >= 10:
##        digits.insert(0, (i % 10))
##        i //= 10
##    digits.insert(0, i)
##    return digits

def integer_to_digits(i):
    """Return a list containing the digits of the specified integer.
    e.g. integer_to_digits(123) returns [1, 2, 3]
    (This implementation is from Dr. Peter Drake, via email on 2016-3-06.)"""
    return [i] if i < 10 else integer_to_digits(i // 10) + [i % 10]

def cube_sum(i):
    """Return the sum of the cubes of the digits of the specified integer."""
    return sum([i ** 3 for i in integer_to_digits(i)])

def chain_153(i):
    """Return a list containing the sequence of integers chaining from the specified integer
    to 153, or a single element consisting of the specified integer itself if it does not
    form a 153 chain."""
    return [i] if i <= 0 or i == 153 or i % 3 != 0 else [i] + chain_153(cube_sum(i))

# Non-recursive implementation of chain_153 method.
#
##def chain_153(i):
##    chain = []
##    while i > 0 and i != 153 and (i % 3) == 0:
##        chain.append(i)
##        i = cube_sum(i)
##    chain.append(i)
##    return chain

def chain_range(start, stop):
    """Prints all the chain_153 sequences within the given [start, stop) range,
    one number chain per line, each chain as a list."""
    for i in range(start, stop):
        print(chain_153(i))

def chain_rangeValid(start, stop):
    """Prints only numbers that are part of valid 153 number chains
    (i.e. integers > 0 and divisible by 3) within the given [start, stop) range,
    one number per line."""
    for i in range(start, stop):
        chain = chain_153(i)
        if len(chain) > 1 or chain[0] == 153:
            for j in chain_153(i):
                print(j)

import sys

if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    stop = int(sys.argv[2])  if len(sys.argv) > 2 else 1
    chain_rangeValid(start, stop)
