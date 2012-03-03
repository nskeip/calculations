import unittest
from spectrum_tests.calculations.spectra_data import spectra, exceptional_spectra
from spectrum.calculations.groups import *
from spectrum_tests.calculations.orders_data import orders, exceptional_orders
from spectrum_tests.parametric import parametrized, parameters

__author__ = 'Daniel Lytkin'

class GroupsTest(unittest.TestCase):
    def test_field_error(self):
        with self.assertRaises(ValueError):
            Field(1)

        with self.assertRaises(ValueError):
            Field(5, 0)

    def test_field_by_order(self):
        f = Field(81)
        self.assertEqual(81, f.order)
        self.assertEqual(3, f.char)
        self.assertEqual(4, f.pow)

    def test_field_by_characteristic(self):
        f = Field(2, 5)
        self.assertEqual(32, f.order)
        self.assertEqual(2, f.char)
        self.assertEqual(5, f.pow)

    def test_sporadic_names(self):
        expected = {"M11", "M12", "M22", "M23", "M24", "J1", "J2", "J3", "J4",
                    "Co1", "Co2", "Co3", "Fi22", "Fi23",
                    "Fi24'", "HS", "McL", "He", "Ru", "Suz", "O'N", "HN", "Ly",
                    "Th", "B", "M", "2F4(2)'"}
        self.assertSetEqual(expected, set(SporadicGroup.all_groups()))

    def test_sporadic_str(self):
        name = "2F4(2)'"
        self.assertEqual(name, str(SporadicGroup(name)))

    def test_alternating_str(self):
        g = AlternatingGroup(51)
        self.assertEqual("Alt(51)", str(g))

    def test_classical_str(self):
        g = ClassicalGroup("PSp", 4, Field(2, 3))
        self.assertEqual("PSp(4, 8)", str(g))

    def test_classical_field(self):
        for g in (ClassicalGroup("PSp", 4, Field(2, 3)),
                  ClassicalGroup("PSp", 4, 2, 3),
                  ClassicalGroup("PSp", 4, 8)):
            self.assertEqual(2, g.field.char)
            self.assertEqual(3, g.field.pow)


@parametrized
class OrdersTest(unittest.TestCase):
    def test_sporadic_order(self):
        expected = 495766656000
        g = SporadicGroup("Co3")
        self.assertEqual(expected, g.order())

    def test_alternating_order(self):
        expected = 653837184000
        g = AlternatingGroup(15)
        self.assertEqual(expected, g.order())

    @parameters(orders.keys())
    def test_classical_orders(self, params):
        g = ClassicalGroup(*params)
        order = orders[params]
        self.assertEqual(order, g.order())

    @parameters(exceptional_orders.keys())
    def test_exceptional_orders(self, params):
        g = ExceptionalGroup(*params)
        order = exceptional_orders[params]
        self.assertEqual(order, g.order())


@parametrized
class SpectraTest(unittest.TestCase):
    def setUp(self):
        self.longMessage = True

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            Group().apex()

    def test_sporadic(self):
        expected = [32, 36, 38, 40, 41, 45, 48, 50, 51, 54, 56,
                    57, 59, 60, 62, 66, 68, 69, 70, 71, 78, 84,
                    87, 88, 92, 93, 94, 95, 104, 105, 110, 119]
        g = SporadicGroup("M")
        self.assertSequenceEqual(expected, g.apex())

    def test_alternating(self):
        expected = [19, 34, 48, 51, 52, 72, 78, 88, 91, 99, 110,
                    120, 126, 132, 165, 168, 180, 195, 231, 315, 420]
        g = AlternatingGroup(21)
        self.assertSequenceEqual(expected, g.apex())

    @parameters(spectra.keys())
    def test_classical_spectra(self, params):
        g = ClassicalGroup(*params)
        apex = spectra[params]
        self.assertSetEqual(set(apex), set(g.apex()))

    @parameters(exceptional_spectra.keys())
    def test_spectra(self, params):
        g = ExceptionalGroup(*params)
        apex = exceptional_spectra[params]
        self.assertSetEqual(set(apex), set(g.apex()))