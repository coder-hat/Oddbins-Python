'''
Generates a Sierpinski Triangle and displays it via a tkinter canvas.
Reference: 
Wikipedia: https://en.wikipedia.org/wiki/Sierpinski_triangle
'''
# NOTE 2018-3-14
# Surprisingly, there doesn't seem to be a "set a pixel" method for a tkinter Canvas.
# This code uses user223850's answer to the Stack Overflow question:
# "How can I draw a point with Canvas in Tkinter?"
# https://stackoverflow.com/questions/39888580/how-can-i-draw-a-point-with-canvas-in-tkinter
#
# NOTE 2018-3-15
# Here's another note about how difficult it is to manipulate single pixels 
# in/on a tkinter Canvas:
# "python tkinter: how to work with pixels?"
# https://stackoverflow.com/questions/12284311/python-tkinter-how-to-work-with-pixels#12287117
#
# Tried using PhotoImage in this code, but got no image -- commented out try, and returned
# to using "truncated" create_oval for now.
#
# NOTE 2018-3-24
# A good discussion of Python Iterators and Generators in Stack Overlow:
# "Difference between Python's Generators and Iterators"
# https://stackoverflow.com/questions/2776829/difference-between-pythons-generators-and-iterators
#
# Rewrote prototype code to encapsulate Sierpeinski-specific code into an iterator class.

from tkinter import *  # For Python version 3.2 or higher.

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

# ---- main program

sp_tri = SierpinskiTriangle(500, 500)

cw, ch = sp_tri.grid_dimensions()

root = Tk()
root.title('Sierpinski Triangle')
canvas_1 = Canvas(root, width=cw, height=ch, background='white')
canvas_1.pack(expand=YES, fill=BOTH)
#img = PhotoImage(width=cw, height=ch)
#canvas_1.create_image((0, 0), image=img, state="normal")

plot_count = 25000
for i in range(1, plot_count):
    ptx, pty = sp_tri.next()
    canvas_1.create_oval(ptx, pty, ptx, pty, width=0, fill='red') # plots a "point"
    #img.put("#ffffff", (ptx, pty)) # "live" update, no explicit update() call required

canvas_1.update() # refresh the drawing on the canvas after all points plotted

root.mainloop()