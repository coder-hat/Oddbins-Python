'''
This .py is is misnamed: orignally it was for a function
that generates the Tribonacci number sequence:
a(n) = a(n-1) + a(n-2) + a(n-3) with a(0)=a(1)=0, a(2)=1.
OEIS: http://oeis.org/A000073
(Wolfram et al.
http://mathworld.wolfram.com/TribonacciNumber.html
give different initial conditions: a(0)=0, a(1)=a=(2)=1.)

However, developing the gen_tribonacci() function revealed
that a generalized function was a trivial modification away.
Hence: gen_n_nacci_sequence()
'''

import argparse
from collections import deque


def gen_tribonacci():
    '''
    Creates an infinite generator for the Tribonacci number sequence
    '''
#   initial_terms = deque([0, 1, 1])  # Wolfram et al. initital terms 
    initial_terms = deque([0, 0, 1])  # OEIS initial terms
    running_terms = deque([], 3)
    while True:
        if initial_terms:
            x = initial_terms.popleft()
            yield x
            running_terms.append(x)
        else:
            x = sum(running_terms)
            yield x
            running_terms.append(x)

def gen_n_nacci_sequence(*initial_terms):
    '''
    Generalized version of the gen_tribonacci function.
    This version creates a generator for an n-nacci sequence
    based on the initial terms provided.
    (e.g. gen_n_nacci_sequence(0 1) creates a Fibonacci generator.)
    '''
    initial_terms = deque(initial_terms)
    running_terms = deque(initial_terms, len(initial_terms))
    while True:
        if initial_terms:
            x = initial_terms.popleft()
            yield x
            running_terms.append(x)
        else:
            x = sum(running_terms)
            yield x
            running_terms.append(x)


if __name__ == "__main__":
    msg = (
        'Prints the terms of the n-nacci sequence defined by the initial terms.\n'
        'Example: the initial terms 0 1 prints the Fibonacci sequence.'
    )
    parser = argparse.ArgumentParser(msg)
    parser.add_argument('-n', type=int, nargs='?', default=10, help='number of terms to print')
    parser.add_argument('initial_terms', type=int, default=[0, 1], nargs='*')
    args = parser.parse_args()

    nacci_generator = gen_n_nacci_sequence(*args.initial_terms)
    print([next(nacci_generator) for i in range(args.n)])
