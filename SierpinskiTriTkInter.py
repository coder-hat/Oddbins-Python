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

from tkinter import Tk  # For Python version 3.2 or higher.
from tkinter import Canvas
from tkinter import YES
from tkinter import BOTH

from SierpinskiTriangle import SierpinskiTriangle

# ---- main program

if __name__ == "__main__":

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