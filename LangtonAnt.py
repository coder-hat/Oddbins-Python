# 2017-10-14
# Langton's Ant as a learning Python and Pygame exercise
# References:
# https://en.wikipedia.org/wiki/Langton%27s_ant
# and, for initial ideas about how Pygame works:
# http://programarcadegames.com/python_examples/f.php?file=simple_graphics_demo.py
# and the Pygram Documentation at:
# http://www.pygame.org/docs/

'''
Langton's Ant program using Python 3 and Pygame
This verison uses a toroidal grid.

This implementation by: Kevin Djang
Developed using: Python 3.6.2 and PyGame 1.9.3
Initial working version: 2017-10-14
'''

import sys
import pygame

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED = (255, 0, 0)

# Frame Rate (for Pygame engine)
FRAMES_PER_SECOND = 15

# Overall dimensions for display are based on the grid dimensions we want.
# In turn, the grid dimensions depend on the dimensions of an indivitual cell,
# plus its border width
CELL_WIDTH = 9 # in pixels
CELL_SIZE = (CELL_WIDTH, CELL_WIDTH) # cells are square
BORDER_WIDTH = 1 # in pixels
CELL_COLS = 80 # in cells
CELL_ROWS = 50 # in cells
WIDTH = (BORDER_WIDTH + CELL_WIDTH) * CELL_COLS + BORDER_WIDTH # in pixels
HEIGHT = (BORDER_WIDTH + CELL_WIDTH) * CELL_ROWS + BORDER_WIDTH # in pixels
SIZE = (WIDTH, HEIGHT)

# Adjacent-cell functions: select the appropriate function by indexing
# the list with the appropriate facing value:
# 0 = above, 1 = right, 2 = below, 3 = left
# The functions assume the grid surface they operate on is a torus:
# column and row values wrap around at the "edges" of the grid.
TORUS_ADJACENT = [
    lambda xy: (xy[0], (xy[1] - 1) % CELL_ROWS), # above (or north)
    lambda xy: ((xy[0] + 1) % CELL_COLS, xy[1]), # right (or east)
    lambda xy: (xy[0], (xy[1] + 1) % CELL_ROWS), # below (or south)
    lambda xy: ((xy[0] - 1) % CELL_COLS, xy[1])  # left  (or west)
]
FACINGS_COUNT = len(TORUS_ADJACENT)

# ---- Functions

def make_grid():
    '''
    Generates a grid with CELL_COLS columns and CEL_ROWS rows of cells,
    and initializes each cell in the grid to its initial state.
    '''
    game_grid = [[WHITE for row in range(CELL_ROWS)] for col in range(CELL_COLS)]
    return game_grid

def move_ant(ant_location, facing):
    '''Computes and returns new (row, col) ant_location based on specified ant_location and facing.'''
    return TORUS_ADJACENT[facing](ant_location)

def get_x_pixel(icol):
    '''
    Computes and returns the display x-coordinate for the upper-left corner of the cell
    in the specified column (icol) of the game grid.
    '''
    return 1 + icol * CELL_WIDTH + icol

def get_y_pixel(irow):
    '''
    Computes and returns the display y-coordinate for the upper-left corner of the cell
    in the specified row (irow) of the game grid.
    '''
    return 1 + irow * CELL_WIDTH + irow

def get_cell_pixels(cell_location):
    '''
    Returns the (x, y) display pixel coordinates that correspond to the specified
    (col, row) grid cell_location.
    '''
    return (get_x_pixel(cell_location[0]), get_y_pixel(cell_location[1]))

def draw_grid(surface, grid):
    '''
    Writes a grid of white cells bordered in gray onto the specified pygame Surface object.
    Assumes surface dimensions will allow an integral number of CELL_WITH-by-CELL_WIDTH cells
    pluse border lines 1 pixel thick.
    '''
    surface.fill(GRAY)
    for row in range(CELL_ROWS):
        ypixel = get_y_pixel(row)
        for col in range(CELL_COLS):
            xpixel = get_x_pixel(col)
            surface.blit(CELL_SURFACES[grid[col][row]], (xpixel, ypixel))

def get_cell_surface(cell_color):
    '''
    Creates a pygame Surface the size of a cell and colors it the specified cell_color.
    '''
    cell_surface = pygame.Surface(CELL_SIZE)
    cell_surface.fill(cell_color)
    return cell_surface

WHITE_CELL = get_cell_surface(WHITE)
BLACK_CELL = get_cell_surface(BLACK)
RED_CELL = get_cell_surface(RED)
CELL_SURFACES = {
    WHITE : WHITE_CELL,
    BLACK : BLACK_CELL,
    RED : RED_CELL
}

# ----- Program Main

def main(argv):
    '''
    Langton's Ant Main Program: runs the langton's ant program in Pygame window
    until user closes the window.
    '''

    ant_cell = (CELL_COLS // 2, CELL_ROWS //2) # Start at cell (x, y) near center of grid
    ant_facing = 0  # 0 = N (up), 1 = E (right), 2 = S (down), 3 = W (left)

    game_grid = make_grid()

    pygame.init() # initialize game engine
    clock = pygame.time.Clock()
    game_screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Langton's Ant")

    draw_grid(game_screen, game_grid)
    game_screen.blit(RED_CELL, get_cell_pixels(ant_cell))
    pygame.display.flip()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Move the ant
        ant_col, ant_row = ant_cell
        if game_grid[ant_col][ant_row] == WHITE:
            # Turn 90 right, flip square, move forward\
            ant_facing = (ant_facing + 1) % FACINGS_COUNT
            game_grid[ant_col][ant_row] = BLACK
            ant_cell = move_ant(ant_cell, ant_facing)
        elif game_grid[ant_col][ant_row] == BLACK:
            # Turn 90 right, flip square, move forward
            ant_facing = (ant_facing - 1) % FACINGS_COUNT
            game_grid[ant_col][ant_row] = WHITE
            ant_cell = move_ant(ant_cell, ant_facing)
        else:
            print("FAIL! Unknown cell value={0}".format(game_grid[ant_col][ant_row]))
            done = True
        # Update the display
        # Important: At this point, ant_cell != (ant_col, ant_row) because ant_cell has moved.
        # (ant_col, ant_row) == prior location, and ant_cell == new location.
        game_screen.blit(CELL_SURFACES[game_grid[ant_col][ant_row]], get_cell_pixels((ant_col, ant_row)))
        game_screen.blit(RED_CELL, get_cell_pixels(ant_cell))
        pygame.display.flip()

        clock.tick(FRAMES_PER_SECOND)

    # Be well-behaved
    pygame.quit()

# ----- Program Entry Point

if __name__ == "__main__":
    main(sys.argv)
