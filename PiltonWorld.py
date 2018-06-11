'''
An implementation of the "Small World" described in Barry Pilton's article:
"A Small World", Manifold, Autumn 1969 issue, pgs 49-53.
https://ianstewartjoat.weebly.com/manifold-5.html
'''

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

    def __init__(self, numberOfCols, numberOfRows):
        self._cols = numberOfCols
        self._rows = numberOfRows
        self.timestep = 0
        self.particles = []

    def do_simulation_step(self):
        t = self.timestep + 1
        self.particles = coalesce_particles(decay_particles(t, coalesce_particles(move_particles(t, self.particles, self._cols, self._rows)), self._cols, self._rows))
        self.timestep = t

    def do_simulation_reset(self):
        self.timestep = 0
        self.particles = []


#---- functions that change the world
#
# NOTE 2018-6-09
# These functions exist only to change PiltonWorld state.
# They should probably be encapsulated inside PiltonWorldState class.
# Encapsulation would reduce the parameter list per function, making the syntax cleaner.
# But, having them global, with explicit parameters, makes unit testing individual functions easier.

def find_molecule(p, particles, cols, rows):
    '''
    Returns the set of PiltonParticles in particles that are edge-adjacent-reachable to each other,
    starting at and including PiltonParticle p.
    Two particles are edge adjacent if they share a common cell edge.
    Diagonal-adjacency (sharing a common cell corner) does not count for molecule membership.
    '''
    molecule = {p}
    adjacents = [o for o in particles if p.is_adjacent_to(o, cols, rows)]
    if not adjacents:
        return molecule
    else:
        for a in adjacents:
            remaining = [o for o in particles if o not in adjacents and o != p]
            molecule.update(find_molecule(a, remaining, cols, rows))
        return molecule

def find_others(p, particles, cols, rows):
    '''
    Returns the set of PiltonParticles in particles that are NOT edge-adjacent-reachable to PiltonParticle p.
    '''
    return [o for o in particles if o not in find_molecule(p, particles, cols, rows)]

def move_particle(t, p, others, cols, rows):
    '''
    Moves (or leaves unmoved) PiltonParticle p, relative to timestep t.
    The others list contains all PiltonParticles currently in the world, but not part of p's molecule.
    Returns either a new particle at the new position, or the same particle if it does not move.
    '''
    if t % p.mass == 0:
        x = (1 + sum([o.x for o in others])) % cols
        y = (1 + sum([o.y for o in others])) % rows
        return PiltonParticle(x, y, p.mass)
    else:
        return p

def move_particles(t, particles, cols, rows):
    '''
    Moves (or leaves unmoved) each PiltonParticle in the particles list relative to the current timestep t.
    Returns a new list of the particles in their new positions.
    '''
    return [move_particle(t, p, find_others(p, particles, cols, rows), cols, rows) for p in particles]

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

def decay_particle(t, p, cols, rows):
    '''
    Determines if and how the specified PiltonParticle p can decay, for timestep t.
    Returns a list containing either p (if no decay occurs) or the PiltonParticles that are p's decay products.
    '''
    decay_products = []
    if t % p.mass == 0:
        xdecays = p.x == (t % cols)
        ydecays = p.y == (t % rows)
        if xdecays and ydecays:
            decay_products.append(PiltonParticle((p.x - 1) % cols, (p.y - 1) % rows, p.mass))
            decay_products.append(PiltonParticle((p.x + 1) % cols, (p.y - 1) % rows, p.mass))
            decay_products.append(PiltonParticle((p.x - 1) % cols, (p.y + 1) % rows, p.mass))
            decay_products.append(PiltonParticle((p.x + 1) % cols, (p.y + 1) % rows, p.mass))
        elif xdecays:
            decay_products.append(PiltonParticle((p.x - 1) % cols, p.y, p.mass))
            decay_products.append(PiltonParticle((p.x + 1) % cols, p.y, p.mass))
        elif ydecays:
            decay_products.append(PiltonParticle(p.x, (p.y - 1) % rows, p.mass))
            decay_products.append(PiltonParticle(p.x, (p.y + 1) % rows, p.mass))
        else:
            decay_products.append(p)
    else:
        decay_products.append(p)
    return decay_products

def decay_particles(t, particles, cols, rows):
    '''
    Returns a new particles list that is the result of applying decay_particle function
    to every PiltonParticle in the specified particles list, relative to timestep t.
    '''
    # NOTE 2018-6-09
    # Hat tip to drake@lclark.edu for making this expression comprehensible.
    return [o for p in particles for o in decay_particle(t, p, cols, rows)]
