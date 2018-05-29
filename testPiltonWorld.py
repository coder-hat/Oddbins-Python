import unittest
import PiltonWorld
from PiltonWorld import PiltonParticle
from PiltonWorld import PiltonWorldState

# NOTE 2018-5-25
# VS Code # "Unhandled exception in thread started by" message occurs
# in the Python Test Log console when tests are run.
# This seems to be an ongoing issue.
# See:
# https:#github.com/Microsoft/vscode-python/issues/78

class TestPiltonWorld(unittest.TestCase):

    def setUp(self):

        # A Dictionary containing successive states (timestep and Particles) of Pilton's Small World
        # listed in the text of the original article, assuming an initial state of: {0, x3y2m1};.
        #
        # The keySet() of timesteps is not contiguous; the original article elided some steps
        # in the example it provided, hence the use of a Dictionary instead of a List.
        #
        # The specific particle values in this data differ from the original article's values at and after t=15.
        # Based on the rules/algorithm described in the article, the example sequence presented in the article itself
        # "goes wrong" at t=15, and is suspect thereafter.  Hand-calculation of the world state from t=15 onwards, 
        # using the articles own rules yields the sequence encoded here.
        self.EXPECT_WORLD_SEQUENCE = {}
        self.EXPECT_WORLD_SEQUENCE[0] = makeParticles((3,2,1))
        self.EXPECT_WORLD_SEQUENCE[1] = makeParticles((0,0), (0,2), (2,0), (2,2), mass=1)
        self.EXPECT_WORLD_SEQUENCE[2] = makeParticles((5,5), (5,3), (3,5), (3,3), mass=1)
        self.EXPECT_WORLD_SEQUENCE[3] = makeParticles((5,5), (5,0), (0,5), (0,0), mass=1)
        self.EXPECT_WORLD_SEQUENCE[4] = makeParticles((6,6), (5,6), (6,5), (5,5), (6,3), (5,3), (3,6), (3,5), (3,3), mass=1)
        self.EXPECT_WORLD_SEQUENCE[5] = makeParticles((0,0,4), (4,2,2), (2,4,2), (6,6,1), (6,4,1), (4,6,1), (4,4,1))
        self.EXPECT_WORLD_SEQUENCE[6] = makeParticles((0,0,5), (2,4,2), (4,2,2), (0,2,1), (2,0,1), (2,2,1))
        self.EXPECT_WORLD_SEQUENCE[7] = makeParticles((0,0,5), (2,4,3), (4,2,3), (2,2,1))
        self.EXPECT_WORLD_SEQUENCE[8] = makeParticles((0,0,6), (2,4,3), (4,2,3))
        self.EXPECT_WORLD_SEQUENCE[9] = makeParticles((0,0,6), (5,3,3), (3,5,3)) 
        self.EXPECT_WORLD_SEQUENCE[12] = makeParticles((2,2,6), (4,6,3), (6,4,3)) 
        self.EXPECT_WORLD_SEQUENCE[15] = makeParticles((2,2,6), (2,0,3), (0,2,3)) 
        self.EXPECT_WORLD_SEQUENCE[18] = makeParticles((3,3,6), (3,5,3), (5,3,3)) 
        self.EXPECT_WORLD_SEQUENCE[21] = makeParticles((3,3,6), (2,6,3), (2,1,3), (6,2,3), (1,2,3)) 
        self.EXPECT_WORLD_SEQUENCE[24] = makeParticles((5,5,6), (6,2,3), (6,0,3), (2,6,3), (0,6,3)) 
        self.EXPECT_WORLD_SEQUENCE[27] = makeParticles((5,5,6), (0,4,3), (0,5,3), (0,0,6), (5,0,3)) 
        self.EXPECT_WORLD_SEQUENCE[30] = makeParticles((3,3,6), (6,1,6), (1,1,6), (1,6,6)) 
        self.EXPECT_WORLD_SEQUENCE[36] = makeParticles((2,2,6), (6,4,6), (4,4,6), (4,6,6)) 
        self.EXPECT_WORLD_SEQUENCE[42] = makeParticles((1,1,6), (4,6,6), (6,6,6), (6,4,6))
        # Bottom half of sequence from the original paper commented-out below.
        # Based on the rules described in the same paper), (this portion of the sequence is actually wrong.
        # Hypothesis: there was a typo or miscalculation made in the original example sequence.
        # By-hand calculation (according to the paper's rules) from t=15 through t=42 gives
        # the bottom half of the sequence above.
        #self.EXPECT_WORLD_SEQUENCE[15] = makeParticles((2,2,6), (3,0,3), (0,3,3)) 
        #self.EXPECT_WORLD_SEQUENCE[18] = makeParticles((3,3,6), (3,5,6), (3,6,3), (5,3,6), (6,3,3), (5,5,6)) 
        #self.EXPECT_WORLD_SEQUENCE[21] = makeParticles((3,3,6), (3,5,6), (6,1,3), (5,3,6), (1,6,3), (5,5,6)) 
        #self.EXPECT_WORLD_SEQUENCE[24] = makeParticles((0,0,6), (0,5,6), (4,2,3), (5,0,6), (2,4,3), (5,5,6)) 
        #self.EXPECT_WORLD_SEQUENCE[27] = makeParticles((0,0,6), (0,1,3), (1,0,3), (0,5,6), (1,5,3), (5,0,6), (5,1,3), (5,5,6)) 
        #self.EXPECT_WORLD_SEQUENCE[30] = makeParticles((3,3,12), (3,1,9), (1,3,9), (6,6,6)) 
        #self.EXPECT_WORLD_SEQUENCE[36] = makeParticles((4,4,12), (4,6,9), (6,4,9), (0,0,6), (0,2,6), (2,0,6), (2,2,6)) 

    def testFindMolecule(self):
        allparticles = makeParticles((6,6), (5,6), (6,5), (5,5), (6,3), (5,3), (3,6), (3,5), (3,3), mass=1)
        expect1 = set(makeParticles((6,6), (5,6), (6,5), (5,5), mass=1))
        expect2 = set(makeParticles((6,3), (5,3), mass=1))
        expect3 = set(makeParticles((3,6), (3,5), mass=1))
        expect4 = set(makeParticles((3,3,1)))
        allexpects = {p: expect1 for p in expect1}
        allexpects.update({p: expect2 for p in expect2})
        allexpects.update({p: expect3 for p in expect3})
        allexpects.update({p: expect4 for p in expect4})
        for p in allexpects:
            expect = allexpects[p]
            actual = PiltonWorld.find_molecule(p, allparticles)
            msg = "p={0} expect={1} actual={2}".format(p, expect, actual)
            self.assertTrue(ignoreOrderEqual(actual, expect), msg)

    def testFindOthers(self):
        allparticles = makeParticles((6,6), (5,6), (6,5), (5,5), (6,3), (5,3), (3,6), (3,5), (3,3), mass=1)
        source1 = set(makeParticles((6,6), (5,6), (6,5), (5,5), mass=1))
        source2 = set(makeParticles((6,3), (5,3), mass=1))
        source3 = set(makeParticles((3,6), (3,5), mass=1))
        source4 = set(makeParticles((3,3,1)))
        others1 = set(makeParticles((6,3), (5,3), (3,6), (3,5), (3,3), mass=1))
        others2 = set(makeParticles((6,6), (5,6), (6,5), (5,5), (3,6), (3,5), (3,3), mass=1))
        others3 = set(makeParticles((6,6), (5,6), (6,5), (5,5), (6,3), (5,3), (3,3), mass=1))
        others4 = set(makeParticles((6,6), (5,6), (6,5), (5,5), (6,3), (5,3), (3,6), (3,5), mass=1))
        allexpects = {p: others1 for p in source1}
        allexpects.update({p: others2 for p in source2})
        allexpects.update({p: others3 for p in source3})
        allexpects.update({p: others4 for p in source4})
        for p in allexpects:
            expect = allexpects[p]
            actual = PiltonWorld.find_others(p, allparticles)
            msg = "p={0} expect={1} actual={2}".format(p, expect, actual)
            self.assertTrue(ignoreOrderEqual(actual, expect), msg)

    def testMoveParticles(self):
        source = makeParticles((0,0,4), (4,2,2), (2,4,2), (6,6,1), (6,4,1), (4,6,1), (4,4,1))
        expect = makeParticles((0,0,4), (0,0,1), (2,4,2), (4,2,2), (0,2,1), (2,0,1), (2,2,1))
        actual = PiltonWorld.move_particles(6, source)
        msg = "source={0} expect={1} actual={2}".format(source, expect, actual)
        self.assertTrue(ignoreOrderEqual(actual, expect), msg)

    def testCoalesceParticles(self):
        source = makeParticles((0,0), (4,2), (2,4), (0,0), (5,5), (2,4), (0,0), (4,2), (0,0), mass=1)
        expect = makeParticles((0,0,4), (4,2,2), (2,4,2), (5,5,1))
        actual = PiltonWorld.coalesce_particles(source)
        msg = "source={0} expect={1} actual={2}".format(source, expect, actual)
        self.assertTrue(ignoreOrderEqual(actual, expect), msg)

    def testDecayParticles(self):
        source = makeParticles((0,0,4), (4,2,2), (2,4,2), (5,5,1))
        expect = makeParticles((0,0,4), (4,2,2), (2,4,2), (6,6,1), (6,4,1), (4,6,1), (4,4,1))
        actual = PiltonWorld.decay_particles(5, source)
        msg = "source={0} expect={1} actual={2}".format(source, expect, actual)
        self.assertTrue(ignoreOrderEqual(actual, expect), msg)

    # "Everybody want to rule the world" - Tears for Fears, 1985 
    def testRunTheWorld(self):
        pwEngine = PiltonWorldState()
    
        max_timestep = max(self.EXPECT_WORLD_SEQUENCE.keys())
        self.assertTrue(max_timestep > 0, "Has-data check")
    
        pwEngine.particles = self.EXPECT_WORLD_SEQUENCE[0]
        self.assertTrue(ignoreOrderEqual(pwEngine.particles, self.EXPECT_WORLD_SEQUENCE[0]), "check initial particles")
        self.assertEqual(pwEngine.timestep, 0, "check initial timestep value")

        while pwEngine.timestep < max_timestep:
            pwEngine.do_simulation_step()
            if pwEngine.timestep in self.EXPECT_WORLD_SEQUENCE:
                expect = self.EXPECT_WORLD_SEQUENCE[pwEngine.timestep]
                actual = pwEngine.particles
                msg = "t={0} expect={1} actual={2}".format(pwEngine.timestep, expect, actual)
                self.assertTrue(ignoreOrderEqual(actual, expect), msg)

#----- Helper functions

def ignoreOrderEqual(particles1, particles2):
    if len(particles1) != len(particles2): return False
    for p in particles1:
        if p not in particles2: 
            # print("p={0} not in {1}".format(p, particles2))
            return False
    return True

def makeParticles(*tuples, mass=None):
    if mass:
        return [PiltonParticle(l[0], l[1], mass) for l in tuples]    
    else:
        return [PiltonParticle(p[0], p[1], p[2]) for p in tuples]

        
if __name__ == '__main__':
    unittest.main()