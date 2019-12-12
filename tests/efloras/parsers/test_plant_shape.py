"""Test plant shape trait notations."""

import unittest
from pylib.shared.trait import Trait
from pylib.efloras.parsers.plant_shape import LEAF_SHAPE, PETIOLE_SHAPE
from pylib.efloras.parsers.plant_shape import HYPANTHIUM_SHAPE, SEPAL_SHAPE


# pylint: disable=too-many-public-methods
class TestPlantShape(unittest.TestCase):
    """Test plant shape trait notations."""

    def test_parse_01(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse('leaf suborbiculate'),
            [Trait(start=0, end=18, part='leaf', value=['orbicular'],
                   raw_value='suborbiculate')])

    def test_parse_02(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse('leaf ovate-suborbicular'),
            [Trait(start=0, end=23, part='leaf', value=['ovate-orbicular'],
                   raw_value='ovate-suborbicular')])

    def test_parse_03(self):
        """TODO."""
        self.assertEqual(
            PETIOLE_SHAPE.parse('petiolule 3–12 mm, narrowly oblanceolate,'),
            [Trait(start=0, end=40, part='petiolule', value=['oblanceolate'],
                   raw_value='narrowly oblanceolate')])

    def test_parse_04(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'Leaves ; blade ovate or orbiculate to '
                'suborbiculate or reniform,'),
            [Trait(start=9, end=63, part='blade',
                   value=['ovate', 'orbicular', 'reniform'],
                   raw_value='ovate or orbiculate to '
                             'suborbiculate or reniform')])

    def test_parse_05(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'Leaves: blade ovate or elongate-ovate to '
                'lanceolate-ovate or ovate-triangular, '),
            [Trait(start=8, end=77, part='blade',
                   value=['ovate', 'elongate-ovate', 'lanceolate-ovate',
                          'ovate-triangular'],
                   raw_value='ovate or elongate-ovate to '
                             'lanceolate-ovate or ovate-triangular')])

    def test_parse_06(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse('Leaves: blade broadly to shallowly triangular'),
            [Trait(start=8, end=45, part='blade', value=['triangular'],
                   raw_value='broadly to shallowly triangular')])

    def test_parse_07(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                '; blade sometimes white-mottled abaxially, suborbiculate to '
                'broadly ovate, depressed-ovate, or reniform, '),
            [Trait(start=2, end=103, part='blade',
                   value=['orbicular', 'ovate', 'reniform'],
                   raw_value='suborbiculate to '
                             'broadly ovate, depressed-ovate, or reniform')])

    def test_parse_08(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse('blade deeply pedately 3-lobed'),
            [])

    def test_parse_09(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'blade <sometimes white-spotted at vein junctions>, '
                'broadly ovate-cordate to triangular-cordate or reniform, '
                'shallowly to deeply palmately '),
            [Trait(start=0, end=106, part='blade',
                   value=['ovate-cordate', 'triangular-cordate', 'reniform'],
                   raw_value='broadly ovate-cordate to triangular-cordate '
                             'or reniform')])

    def test_parse_10(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse('Leaf blades 2–7 cm wide, lobe apex rounded'),
            [])

    def test_parse_11(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse('Leaf blades mostly orbiculate, '
                             'deeply to shallowly lobed,'),
            [Trait(start=0, end=29, part='leaf blades', value=['orbicular'],
                   raw_value='mostly orbiculate')])

    def test_parse_12(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'Leaves: petiole 1–3(–4.5) cm; blade pentagonal-angulate to '
                'reniform-angulate or shallowly 5-angulate,'),
            [Trait(start=30, end=100, part='blade',
                   value=['polygonal', 'reniform-polygonal'],
                   raw_value='pentagonal-angulate to '
                             'reniform-angulate or shallowly 5-angulate')])

    def test_parse_13(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'blade lanceolate to narrowly or broadly lanceolate '
                'or elliptic-lanceolate, '),
            [Trait(start=0, end=73, part='blade',
                   value=['lanceolate', 'elliptic-lanceolate'],
                   raw_value='lanceolate to narrowly or broadly lanceolate '
                             'or elliptic-lanceolate')])

    def test_parse_14(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'blade broadly ovate to rounded-cordate, subreniform, '
                'or deltate'),
            [Trait(start=0, end=63, part='blade',
                   value=['ovate', 'orbicular-cordate', 'reniform',
                          'deltoid'],
                   raw_value='broadly ovate to rounded-cordate, subreniform, '
                             'or deltate')])

    def test_parse_15(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'blade orbic-ulate to pentagonal,'),
            [Trait(start=0, end=31, part='blade',
                   value=['orbicular', 'polygonal'],
                   raw_value='orbic-ulate to pentagonal')])

    def test_parse_16(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'blade pen-tagonal'),
            [Trait(start=0, end=17, part='blade',
                   value=['polygonal'], raw_value='pen-tagonal')])

    def test_parse_17(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'Leaves usually in basal rosettes, sometimes cauline, '
                'usually alternate, sometimes opposite '),
            [Trait(start=0, end=51, part='leaves',
                   location=['basal', 'cauline'],
                   value=['rosettes'],
                   raw_value='basal rosettes, sometimes cauline')])

    def test_parse_18(self):
        """TODO."""
        self.assertEqual(
            HYPANTHIUM_SHAPE.parse('hypanthium cupulate'),
            [Trait(start=0, end=19, part='hypanthium',
                   value=['cup-shaped'], raw_value='cupulate')])

    def test_parse_19(self):
        """TODO."""
        self.assertEqual(
            HYPANTHIUM_SHAPE.parse(
                'hypanthium cupulate to shallowly campanulate;'),
            [Trait(start=0, end=44, part='hypanthium',
                   value=['cup-shaped', 'campanulate'],
                   raw_value='cupulate to shallowly campanulate')])

    def test_parse_20(self):
        """TODO."""
        self.assertEqual(
            HYPANTHIUM_SHAPE.parse(
                'hypanthium subcylindric to narrowly funnelform;'),
            [Trait(start=0, end=46, part='hypanthium',
                   value=['cylindrical', 'funnelform'],
                   raw_value='subcylindric to narrowly funnelform')])

    def test_parse_21(self):
        """TODO."""
        self.assertEqual(
            HYPANTHIUM_SHAPE.parse(
                'hypanthium narrowly campanulate to cylindric '
                '[obtriangular];'),
            [Trait(
                start=0, end=58, part='hypanthium',
                value=['campanulate', 'cylindric', 'obtriangular'],
                raw_value='narrowly campanulate to cylindric [obtriangular')])

    def test_parse_22(self):
        """TODO."""
        self.assertEqual(
            SEPAL_SHAPE.parse('sepals linear-subulate, 3–5 mm; '),
            [Trait(start=0, end=22, part='sepals',
                   value=['linear-subulate'],
                   raw_value='linear-subulate')])

    def test_parse_23(self):
        """TODO."""
        self.assertEqual(
            SEPAL_SHAPE.parse('sepals cylindrical, peltate, semiterete, '
                              'subcylindrical, subpeltate, subterete, '
                              'subulate, terete'),
            [Trait(start=0, end=96, part='sepals',
                   value=['cylindrical', 'peltate', 'semiterete',
                          'subpeltate', 'subterete',
                          'subulate', 'terete'],
                   raw_value='cylindrical, peltate, semiterete, '
                             'subcylindrical, subpeltate, subterete, '
                             'subulate, terete')])

    def test_parse_24(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'blade unlobed or palmately, pedately, or pinnately lobed'),
            [])

    def test_parse_25(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse(
                'Pistillate flowers: ovary usually 1-locular, ovoid to '
                'elliptic-ovoid or subglobose'),
            [])

    def test_parse_26(self):
        """TODO."""
        self.assertEqual(
            LEAF_SHAPE.parse('Leaves in basal rosette and cauline'),
            [Trait(start=0, end=35, part='leaves',
                   location=['basal', 'cauline'],
                   value=['rosette'],
                   raw_value='basal rosette and cauline')])
