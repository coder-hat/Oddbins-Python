'''
= 2018-6-16
Recaman's Sequence -- so named by N.J.A. Sloane
Description:
    a(0) = 0; for n > 0, a(n) = a(n-1) - n
if positive and not already in the sequence, otherwise 
    a(n) = a(n-1) + n.
References:
1. The Online Encyclopedia of Integer Sequences, https://oeis.org/A005132
2. "The Slightly Spooky Recaman Sequence - Numberphile, https://www.youtube.com/watch?v=FGC5TdIiT9U"
'''

# First terms of the Recaman sequence from OEIS (for checking code results):
expect = (0, 1, 3, 6, 2, 7, 13, 20, 12, 21, 11, 22, 10, 23, 9, 24, 8, 25, 43, 62, 42, 63, 41, 18, 42, 17, 43, 16, 44, 15, 45, 14, 46, 79, 113, 78, 114, 77, 39, 78, 38, 79, 37, 80, 36, 81, 35, 82, 34, 83, 33, 84, 32, 85, 31, 86, 30, 87, 29, 88, 28, 89, 27, 90, 26, 91, 157, 224, 156, 225, 155)

def recaman1(n):
    actual = [0]
    for i in range(1, n):
        a_last = actual[i-1]
        a_next = a_last - i
        if a_next < 0: 
            actual.append(a_last + i)
        elif a_next not in actual:
            actual.append(a_next)
        else:
            actual.append(a_last + i)
    return actual

# Question: 
# Is there any way to generate the sequence without storing all of the earlier elements of the sequence?
# 
# The following doesn't work because the "unused" set ends up containing numbers that are already used.
# I haven't thought of a way for the code to "know" that the numbers are already used without keeping a list of the used numbers.
# It is possible that is an impossible thing -- but I haven't read or come up with a proof for that either.

def recaman_generator():
    '''
    WARNING: Does NOT actually produce a proper Recaman sequence !!!
    '''
    unused = set()
    i = 0
    a_now = 0
    while True:
        print("yield={0}".format(a_now), end='')
        yield a_now
        i += 1
        a_next = a_now - i
        if a_next < 0:
            a_next = a_now + i
            {unused.add(j) for j in range(i, a_next)}
        elif a_next in unused:
            unused.remove(a_next)
        else:
            a_next = a_now + i
        a_now = a_next
        print(" i={0} a_next={1} unused={2}".format(i, a_next, unused))

if __name__ == "__main__":
    a1 = recaman1(len(expect))

    rg = recaman_generator()
    a2 = [next(rg) for i in range(len(expect))]

    for i in range(0, len(expect)):
        print(" [expect={0} a1={1} a2={2}: {3} {4}]".format(expect[i], a1[i], a2[i], (expect[i] == a1[i]), expect[i] == a2[i]))
        if not expect[i] == a2[i]:
            break
    #print()
