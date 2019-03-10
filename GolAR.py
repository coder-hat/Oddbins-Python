# Dr. Alex Rienhart's Racket code for Conway's Game of Life translated into Python 3.
# See:
# "A flexible implementation of Conway's Game of Life", 2016-1-25
# https://www.refsmmat.com/posts/2016-01-25-conway-game-of-life.html
#
# I ported the code from the above article as an exercise to help me understand
# both Racket and Python a bit better.
#
# Additional kudos:
# Peter Drake,
# https://college.lclark.edu/live/profiles/1906-peter-drake
# untangled nested list conprehension syntax for me.

from collections import Counter
from collections.abc import Iterable
from itertools import chain

def conway_rules(number_of_neighbors, is_alive):
    '''Returns True if number_of_neighbors and is_alive status meet Conway's Game of Life aliveness criteria.'''
    return (number_of_neighbors == 2) or (number_of_neighbors == 3) if is_alive else (number_of_neighbors == 3)

def neighbors_rect(location):
    '''Returns location tuple (x,y)'s 8 neighbor locations as a list of (x,y) tuples.'''
    x, y = location
    return [(x + dx, y + dy) for dy in [-1, 0, 1] for dx in [-1, 0 ,1] if not (dx == 0 and dy == 0)]

# Alex R.'s Racket code contains a function named count-occurrences,
# however, Python's collections.Counter peforms exactly that function.

def step(rules, neighbors, live_cells):
    '''Applies rules and neighbors functions to live_cells, returing next generation of live cells.'''
    # get dictionary with key=location val=location_count
    num_neighbors = Counter(list(chain.from_iterable(neighbors(live_cell) for live_cell in live_cells)))
    # apply rules to each cell to build next generation
    return [cell for cell, count in num_neighbors.items() if rules(count, (cell in live_cells))]