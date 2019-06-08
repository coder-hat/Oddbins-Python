'''
Functions that generate the Tribonacci number sequence:
a(n) = a(n-1) + a(n-2) + a(n-3) with a(0)=a(1)=0, a(2)=1.
OEIS: http://oeis.org/A000073
Wolfram et al.
http://mathworld.wolfram.com/TribonacciNumber.html
give different initial conditions: a(0)=0, a(1)=a=(2)=1.
'''
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

if __name__ == "__main__":
    tri = gen_tribonacci()
    print([next(tri) for i in range(25)])
