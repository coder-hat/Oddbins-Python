'''
An implementation of the "Small World" described in Barry Pilton's article:
"A Small World", Manifold, Autumn 1969 issue, pgs 49-53.
https://ianstewartjoat.weebly.com/manifold-5.html
'''

_CELL_COLS = 7
_CELL_ROWS = 7

#----- particle class, particle class, particle class has location and mass!

class PiltonParticle(tuple):
    '''
    Contains the state (2-d position and mass) of a single Pilton Particle.
    '''
    def __new__(cls, x, y, mass):
        return tuple.__new__(cls, (x, y, mass))
    
    @property
    def x(self): 
        '''Returns the x-coordinate of this particle's 2-d location.'''
        return self[0]
    
    @property
    def y(self):
        '''Returns the y-coordinate of this particle's 2-d location.'''
        return self[1]

    @property
    def mass(self):
        '''Returns the mass of this particle.'''
        return self[2]

    @property
    def location(self):
        '''Returns the location of this particle as an (x, y) tuple.'''
        return self[0:2]

    def is_colocated(self, other):
        '''
        Returns True if self and other have the same x and y values.
        Otherwise, returns False.
        '''
        return self.x == other.x and self.y == other.y

    def is_adjacent_to(self, other, col_count, row_count):
        '''
        Determines whether self is edge-adjacent to other within the context of the specified grid dimensions.
        Returns True if self is edge-adjacent to other, False otherwise.
        '''
        x_match = (other.x == (self.x - 1) % col_count) or (other.x == (self.x + 1) % col_count)
        y_match = (other.y == (self.y - 1) % row_count) or (other.y == (self.y + 1) % row_count)
        return (x_match and other.y == self.y) or (y_match and other.x == self.x)

    # When overriding __str__, "The goal of str is to be [human] readable ..."    
    # https://stackoverflow.com/questions/1436703/difference-between-str-and-repr
    def __str__(self):
        '''
        Returns a human-readable, compact description of this PiltonParticle's state.
        '''
        return "x{0}y{1}m{2}".format(self.x, self.y, self.mass)

#---- the state of the world

class PiltonWorldState:

    def __init__(self):
        self.timestep = 0
        self.particles = []

    def do_simulation_step(self):
        t = self.timestep + 1
        self.particles = coalesce_particles(decay_particles(t, coalesce_particles(move_particles(t, self.particles))))
        self.timestep = t

#---- functions that change the world
#
# NOTE 2018-6-09
# These functions exist only to change PiltonWorld state.
# They should probably be encapsulated inside PiltonWorldState class.
# But, if they were member functions, there'd be no sense in passing in timestep (or particles, in some cases).
# Having them global makes the parameters explicit, which in turn makes unit testing them easier.
# However, some of these "global" functions rely on the global column and row dimensions,
# and that's something it would be nice to allow the user to modify per world in a GUI setting,
# so they're not *really* independent as-is.

def find_molecule(p, particles):
    '''
    Returns the set of PiltonParticles in particles that are edge-adjacent-reachable to each other,
    starting at and including PiltonParticle p.
    Two particles are edge adjacent if they share a common cell edge.
    Diagonal-adjacency (sharing a common cell corner) does not count for molecule membership.
    '''
    molecule = {p}
    adjacents = [o for o in particles if p.is_adjacent_to(o, _CELL_COLS, _CELL_ROWS)]
    if not adjacents:
        return molecule
    else:
        for a in adjacents:
            remaining = [o for o in particles if o not in adjacents and o != p]
            molecule.update(find_molecule(a, remaining))
        return molecule

def find_others(p, particles):
    '''
    Returns the set of PiltonParticles in particles that are NOT edge-adjacent-reachable to PiltonParticle p.
    '''
    return [o for o in particles if o not in find_molecule(p, particles)]

def move_particle(t, p, others):
    '''
    Moves (or leaves unmoved) PiltonParticle p, relative to timestep t.
    The others list contains all PiltonParticles currently in the world, but not part of p's molecule.
    Returns either a new particle at the new position, or the same particle if it does not move.
    '''
    if t % p.mass == 0:
        x = (1 + sum([o.x for o in others])) % _CELL_COLS
        y = (1 + sum([o.y for o in others])) % _CELL_ROWS
        return PiltonParticle(x, y, p.mass)
    else:
        return p

def move_particles(t, particles):
    '''
    Moves (or leaves unmoved) each PiltonParticle in the particles list relative to the current timestep t.
    Returns a new list of the particles in their new positions.
    '''
    return [move_particle(t, p, find_others(p, particles)) for p in particles]

def coalesce_particles(particles):
    '''
    Takes the specified list of PiltonParticles and returns a new list 
    by replacing all co-located particles with a single particle with
    the same location, and the sum of the co-located particles mass.
    '''
    d = {}
    for p in particles:
        d[p.location] = d[p.location] + p.mass if p.location in d else p.mass
    return [PiltonParticle(k[0], k[1], v) for (k, v) in d.items()]

def decay_particle(t, p):
    '''
    Determines if and how the specified PiltonParticle p can decay, for timestep t.
    Returns a list containing either p (if no decay occurs) or the PiltonParticles that are p's decay products.
    '''
    decay_products = []
    if t % p.mass == 0:
        xdecays = p.x == (t % _CELL_COLS)
        ydecays = p.y == (t % _CELL_ROWS)
        if xdecays and ydecays:
            decay_products.append(PiltonParticle((p.x - 1) % _CELL_COLS, (p.y - 1) % _CELL_ROWS, p.mass))
            decay_products.append(PiltonParticle((p.x + 1) % _CELL_COLS, (p.y - 1) % _CELL_ROWS, p.mass))
            decay_products.append(PiltonParticle((p.x - 1) % _CELL_COLS, (p.y + 1) % _CELL_ROWS, p.mass))
            decay_products.append(PiltonParticle((p.x + 1) % _CELL_COLS, (p.y + 1) % _CELL_ROWS, p.mass))
        elif xdecays:
            decay_products.append(PiltonParticle((p.x - 1) % _CELL_COLS, p.y, p.mass))
            decay_products.append(PiltonParticle((p.x + 1) % _CELL_COLS, p.y, p.mass))
        elif ydecays:
            decay_products.append(PiltonParticle(p.x, (p.y - 1) % _CELL_ROWS, p.mass))
            decay_products.append(PiltonParticle(p.x, (p.y + 1) % _CELL_ROWS, p.mass))
        else:
            decay_products.append(p)
    else:
        decay_products.append(p)
    return decay_products

def decay_particles(t, particles):
    '''
    Returns a new particles list that is the result of applying decay_particle function
    to every PiltonParticle in the specified particles list, relative to timestep t.
    '''
    # NOTE 2018-6-09
    # Hat tip to drake@lclark.edu for making this expression comprehensible.
    return [o for p in particles for o in decay_particle(t, p)]
