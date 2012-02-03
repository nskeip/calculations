import unittest
from spectrum.graph.drawing import PickedState

__author__ = 'Daniel Lytkin'


class PickedStateTest(unittest.TestCase):
    def setUp(self):
        self.state = PickedState()

    def test_pick(self):
        s = self.state
        self.assertSetEqual(set(), s.get_picked())

        self.assertFalse(s.is_picked(42))
        s.pick(42)
        self.assertTrue(s.is_picked(42))

        s.pick(42, False)
        self.assertFalse(s.is_picked(42))

        for i in (42, 43, 44):
            s.pick(i)
        self.assertSetEqual({42, 43, 44}, s.get_picked())

        s.clear()
        self.assertSetEqual(set(), s.get_picked())




