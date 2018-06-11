'''
GUI for running 7x7 Pilton World Simulation
'''
from tkinter import Tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import StringVar
from tkinter import BooleanVar
from tkinter import Text
from PiltonWorld import PiltonParticle
from PiltonWorld import PiltonWorldState

# ----- Core dimensions
_cols = 7
_rows = 7
_cell_width_pixels = 35  # cells are square, so height == width
_grid_width_pixels = _cols * _cell_width_pixels + 1
_grid_height_pixels = _rows * _cell_width_pixels + 1

# ----- Model

starting_particles = [PiltonParticle(3,2,1)]

ps = PiltonWorldState(_cols, _rows)
ps.particles = starting_particles

# ----- Controller

status_prefix = "World {0}x{1}".format(_cols, _rows)

def particles_text(ps):
    return str([str(p) for p in ps.particles]).replace("'","")

def update_display():
    textcanvas.delete('all')
    textcanvas.create_text(1, 1, anchor='nw', width=(textcanvas.winfo_width() - 2), text=particles_text(ps))

    gridcanvas.delete('all')
    for p in ps.particles:
        gx0 = p.x * _cell_width_pixels
        gy0 = p.y * _cell_width_pixels
        gx1 = gx0 + _cell_width_pixels
        gy1 = gy0 + _cell_width_pixels
        gridcanvas.create_rectangle(gx0, gy0, gx1, gy1, fill='red', outline=_backcolor)

    statustext.set("{0} : t={1} particles={2}".format(status_prefix, ps.timestep, len(ps.particles)))

def do_step():
    ps.do_simulation_step()
    update_display()

# NOTE 2018-6-10
# WARNING !!! Start/Stop doesn't work !!!
# Need to learn about the equivalent of SwingWorker for Python Tkinter

# def do_start():
#     sim_running.set(True)
#     while sim_running.get():
#         do_step()

# def do_stop():
#     sim_running.set(False)

def do_reset():
    ps.do_simulation_reset()
    ps.particles = starting_particles
    update_display()

# ----- View

_backcolor = 'lightgray'

root = Tk()
root.title("Pilton Small World")

statustext = StringVar()

# sim_running = BooleanVar()
# sim_running.set(False)

mainframe = ttk.Frame(root, padding='3 3 3 3')
mainframe.grid(column=0, row=0, sticky="nsew")
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

lblstatus = ttk.Label(mainframe, textvariable=statustext)
lblstatus.grid(column=0, row=0, sticky='ew')

gridcanvas = Canvas(mainframe, width=_grid_width_pixels, height=_grid_height_pixels)
gridcanvas.configure(bg=_backcolor, bd=0, highlightthickness=0)
gridcanvas.grid(column=0, row=1, columnspan=2, sticky='w')

textcanvas = Canvas(mainframe, width=_grid_width_pixels, height=_grid_height_pixels)
textcanvas.configure(bg='cyan', bd=0, highlightthickness=0)
textcanvas.grid(column=2, row=1, columnspan=2, sticky='e')

# NOTE 2018-6-10
# Would prefer to use a Tk Text widget for the particles text display area.
# However, had difficulty making it read-only, and sizing it same as grid display to its left.
# Have read the following, but their suggestions did not work in this code.
#
# See:
# "Is there a way to make the Tkinter text widget read only?"
# https://stackoverflow.com/questions/3842155/is-there-a-way-to-make-the-tkinter-text-widget-read-only
# See:
# Specifying the dimensions of a Tkinter Text Widget in pixels?
# https://stackoverflow.com/questions/10463826/specifying-the-dimensions-of-a-tkinter-text-widget-in-pixels
# See:
# "Specify the dimensions of a Tkinter text box in pixels"
# https://stackoverflow.com/questions/14887610/specify-the-dimensions-of-a-tkinter-text-box-in-pixels

# textframe = ttk.Frame(mainframe, width=_grid_width_pixels, height=_grid_height_pixels)
# textframe.grid_propagate(False)
# textframe.grid(column=1, row=1, sticky='n, s, e')

# txtParticles = Text(textframe, wrap='word', bg='yellow')
# txtParticles.grid_propagate(False)
# txtParticles.insert('end', "{0}".format(ps.particles))

btnstep = ttk.Button(mainframe, text="STEP", command=do_step)
btnstep.grid(column=0, row=2, sticky='w')

# NOTE 2018-6-10
# WARNING !!! Start/Stop doesn't work !!!
# Need to learn about the equivalent of SwingWorker for Python Tkinter

# btnStart = ttk.Button(mainframe, text="START", command=do_start)
# btnStart.grid(column=1, row=2, sticky='w')

# btnStop = ttk.Button(mainframe, text="STOP", command=do_stop)
# btnStop.grid(column=2, row=2, sticky='w')

btnReset = ttk.Button(mainframe, text="RESET", command=do_reset)
btnReset.grid(column=3, row=2, sticky='e')

for child in mainframe.winfo_children():
    child.grid_configure(padx=1, pady=1)

if __name__ == '__main__':
    update_display()
    mainframe.mainloop()
