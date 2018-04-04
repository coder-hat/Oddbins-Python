'''
Sierpinski Triangle Code.
Wikipedia: https://en.wikipedia.org/wiki/Sierpinski_triangle
'''
# NOTE 2018-3-24
# A good discussion of Python Iterators and Generators in Stack Overlow:
# "Difference between Python's Generators and Iterators"
# https://stackoverflow.com/questions/2776829/difference-between-pythons-generators-and-iterators
#
# Rewrote prototype code to encapsulate Sierpeinski-specific code into an iterator class.

import random

class SierpinskiTriangle:
    '''
    An iterator class that holds enough state to generated a sequence of points that, when plotted,
    will display a Sierpinski Triangle.
    The algorithm used is described in Wikipedia:
    https://en.wikipedia.org/wiki/Sierpinski_triangle
    1. Take 3 points in a plane to form a triangle, you need not draw it.
    2. Randomly select any point inside the triangle and consider that your current position.
    3. Randomly select any one of the 3 vertex points.
    4. Move half the distance from your current position to the selected vertex.
    5. Plot the current position.
    6. Repeat from step 3.
    '''
    def __init__(self, grid_width, grid_height):
        '''
        Constructs a Sierpinski Triangle iterator object with 3 anchor points,
        and a bounding rectangle with dimensions of grid_width, grid_height.
        The 1st anchor point is a x-location along the top of the bounding rectangle.
        The 2nd anchor point is a y-location along the lower-half of the left side of the bounding rectangle.
        The 3rd anchor point is a y-location along the lower-half of the right side of the bounding rectangle.
        '''
        self.grid_width = grid_width
        self.grid_height = grid_height
        half_grid_height = grid_height // 2
        p1 = (random.randint(1, self.grid_width - 1), 0) # 1st point
        p2 = (0, random.randint(1, half_grid_height) + half_grid_height - 1) # 2nd point
        p3 = (self.grid_width - 1, random.randint(0, half_grid_height) + half_grid_height - 1) # 3rd point
        self.anchors = (p1, p2, p3)
        self.p_now = (random.randint(1, self.grid_width - 1), random.randint(1, self.grid_height - 1))

    def grid_dimensions(self):
        '''Returns the (grid_width, grid_height) of this object.'''
        return (self.grid_width, self.grid_height)

    def __iter__(self):
        return self

    def next(self):
        '''
        Computes a new "inner" point based on one of this object's randomly selected
        anchor points and the current inner point, and returns the new (x, y) point.
        '''
        # Pick one of the three anchor points
        anc_x, anc_y = self.anchors[random.randint(0,len(self.anchors)-1)]
        now_x, now_y = self.p_now
        # Compute new point half-way between the chosen anchor point and the current ("now") point.
        new_x = min(anc_x, now_x) + (abs(anc_x - now_x) // 2)
        new_y = min(anc_y, now_y) + (abs(anc_y - now_y) // 2)
        # Replace current point with new point
        self.p_now = (new_x, new_y)
        return self.p_now
