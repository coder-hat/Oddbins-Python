'''
Generates a Sierpinski Triangle and displays it via MatPlotLib.
Reference: 
Wikipedia: https://en.wikipedia.org/wiki/Sierpinski_triangle
'''
# NOTE 2018-3-26
# The problem with this approach is that a scatter() plot with s=1 
# does _not_ guarantee each plot point will be 1 pixel in size.
# Maybe adjusting the figure(...) parameters will help?
# Haven't had a chance to read up on this yet.

import matplotlib.pyplot as plt

from SierpinskiTriangle import SierpinskiTriangle

if __name__ == "__main__":
    sp_tri = SierpinskiTriangle(500, 500)
    number_of_points = 25000
    xpts = []
    ypts = []
    for i in range(0, number_of_points):
        x, y = sp_tri.next()
        xpts.append(x)
        ypts.append(y)
    #plt.figure()
    plt.scatter(xpts, ypts, edgecolor='none', c='red', s=1)
    plt.show()
