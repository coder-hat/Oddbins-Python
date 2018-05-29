import unittest
from PiltonWorld import PiltonParticle

# NOTE 2018-5-25
# VS Code # "Unhandled exception in thread started by" message occurs
# in the Python Test Log console when tests are run.
# This seems to be an ongoing issue.
# See:
# https://github.com/Microsoft/vscode-python/issues/78

class TestPiltonParticle(unittest.TestCase):

    def testParticleProperties(self):
        p = PiltonParticle(1,2,3)
        self.assertEqual(p.x, 1, "x")
        self.assertEqual(p.y, 2, "y")
        self.assertEqual(p.mass, 3, "mass")

    def testParticleEquality(self):
        p = PiltonParticle(1,2,3)
        self.assertEqual(p, PiltonParticle(1,2,3), "equal")
        self.assertNotEqual(p, PiltonParticle(4,2,3), "x differs")
        self.assertNotEqual(p, PiltonParticle(1,4,3), "y differs")
        self.assertNotEqual(p, PiltonParticle(1,2,4), "mass differs")

    def testParticleImmutability(self):
        p = PiltonParticle(1,2,3)
        with self.assertRaises(AttributeError):
            p.x = 4
        with self.assertRaises(AttributeError):
            p.y = 4
        with self.assertRaises(AttributeError):
            p.mass = 4
        with self.assertRaises(AttributeError):
            p.location = (1,2)

    def testParticleIsColocated(self):
        p = PiltonParticle(1,2,3)
        others = { PiltonParticle(1,2,5) : True, PiltonParticle(2,2,3) : False }
        for o in others:
            msg = "p={0} o={1} expect={2}".format(p, o, others[o])
            self.assertEqual(p.is_colocated(o), others[o], msg)
    
    def testParticleLocation(self):
        p1 = PiltonParticle(1,2,3)
        p2 = PiltonParticle(2,1,3)
        p3 = PiltonParticle(1,2,4)
        self.assertTrue(p1.location != p2.location, "different locations")
        self.assertTrue(p1.location == p3.location, "same location")
        
if __name__ == '__main__':
    unittest.main()