import unittest

from spectrum.calculations.groups import GroupType


class GroupTypeTest(unittest.TestCase):
    def test_caption(self):
        self.assertEqual(GroupType.ALTERNATING.caption, 'Alternating')
        self.assertEqual(GroupType.CLASSICAL.caption, 'Classical')
        self.assertEqual(GroupType.EXCEPTIONAL.caption, 'Exceptional')
        self.assertEqual(GroupType.SPORADIC.caption, 'Sporadic')
