import unittest
from pylib.efloras.trait import Trait
from pylib.efloras.parsers.plant_size import LEAF_SIZE, PETIOLE_SIZE
from pylib.efloras.parsers.plant_size import PETAL_SIZE, SEPAL_SIZE
from pylib.efloras.parsers.plant_size import FLOWER_SIZE, HYPANTHIUM_SIZE


class TestPlantSize(unittest.TestCase):

    def test_parse_01(self):
        """It parses a cross measurement."""
        self.assertEqual(
            LEAF_SIZE.parse('Leaf (12-)23-34 × 45-56 cm'),
            [Trait(start=0, end=26, part='leaf',
                   min_length=120, low_length=230, high_length=340,
                   low_width=450, high_width=560)])

    def test_parse_02(self):
        """Units are required."""
        self.assertEqual(
            LEAF_SIZE.parse('(12-)23-34 × 45-56'),
            [])

    def test_parse_03(self):
        """It parses a range simple measurement."""
        self.assertEqual(
            LEAF_SIZE.parse('blade 1.5–5(–7) cm'),
            [Trait(part='blade', start=0, end=18,
                   low_length=15, high_length=50, max_length=70)])

    def test_parse_04(self):
        """It does not allow trailing dashes."""
        self.assertEqual(
            LEAF_SIZE.parse('shallowly to deeply 5–7-lobed'),
            [])

    def test_parse_05(self):
        """It get a dimension."""
        self.assertEqual(
            LEAF_SIZE.parse('leaf 4–10 cm wide'),
            [Trait(start=0, end=17, low_length=40, high_length=100,
                   part='leaf', dimension='wide')])

    def test_parse_06(self):
        """It does not interpret fractions as a range."""
        self.assertEqual(
            LEAF_SIZE.parse('sinuses 1/5–1/4 to base'),
            [])

    def test_parse_07(self):
        """It allows a simple range."""
        self.assertEqual(
            PETIOLE_SIZE.parse('petiolules 2–5 mm'),
            [Trait(part='petiolules', start=0, end=17,
                   low_length=2, high_length=5)])

    def test_parse_08(self):
        """It pickes up multiple measurements."""
        self.assertEqual(
            PETIOLE_SIZE.parse(
                'petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm.'),
            [Trait(part='petiolules', start=0, end=17,
                   low_length=2, high_length=5),
             Trait(part='petioles', start=37, end=54,
                   low_length=16, high_length=28)])

    def test_parse_09(self):
        """It allows a simple range."""
        self.assertEqual(
            PETIOLE_SIZE.parse('Leaves: petiole 2–15 cm;'),
            [Trait(part='petiole', start=8, end=23,
                   low_length=20, high_length=150)])

    def test_parse_10(self):
        """It allows alternate opening and closing brackets."""
        self.assertEqual(
            PETIOLE_SIZE.parse(
                'oblong [suborbiculate], petiole [5–]7–25[–32] mm, glabrous,'),
            [Trait(start=24, end=48, part='petiole',
                   low_length=7, high_length=25,
                   min_length=5, max_length=32)])

    def test_parse_11(self):
        """It handles different units for width and length."""
        self.assertEqual(
            LEAF_SIZE.parse('leaf 2–4 cm × 2–10 mm'),
            [Trait(start=0, end=21, part='leaf',
                   low_length=20, high_length=40,
                   low_width=2, high_width=10)])

    def test_parse_12(self):
        """It does not pick up a lobe measurement."""
        self.assertEqual(
            LEAF_SIZE.parse('deeply to shallowly lobed, 4–5(–7) cm wide,'),
            [])

    def test_parse_13(self):
        """It handles a range after a lobe notation."""
        self.assertEqual(
            PETIOLE_SIZE.parse('Leaves 3-foliolate, lateral pair of leaflets '
                               'deeply lobed, petiolules 2–5 mm,'),
            [Trait(start=20, end=76, part='petiolules', location='lateral',
                   low_length=2, high_length=5)])

    def test_parse_14(self):
        self.assertEqual(
            LEAF_SIZE.parse('terminal leaflet 3–5 cm, blade '
                            'narrowly lanceolate, petiolule 3–12 mm,'),
            [Trait(start=0, end=23, location='terminal', part='leaflet',
                   low_length=30, high_length=50)])

    def test_parse_15(self):
        self.assertEqual(
            LEAF_SIZE.parse('shallowly 3–5(–7)-lobed, '
                            '5–25 × (8–)10–25(–30) cm,'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            LEAF_SIZE.parse('(3–)5-lobed, 6–20(–30) × 6–25 cm,'),
            [])

    def test_parse_17(self):
        self.assertEqual(
            LEAF_SIZE.parse('blade deeply pedately 3-lobed, 2–6 cm wide'),
            [Trait(start=0, end=42, part='blade', dimension='wide',
                   low_length=20, high_length=60)])

    def test_parse_18(self):
        self.assertEqual(
            PETIOLE_SIZE.parse('petiole to 11 cm;'),
            [Trait(start=0, end=16, part='petiole', high_length=110)])

    def test_parse_19(self):
        self.assertEqual(
            LEAF_SIZE.parse('blade ovate to depressed-ovate or flabellate, '
                            '5-17(-20) × (3-)6-16 mm'),
            [Trait(start=0, end=69, part='blade',
                   low_length=5, high_length=17, max_length=20,
                   min_width=3, low_width=6, high_width=16)])

    def test_parse_20(self):
        self.assertEqual(
            LEAF_SIZE.parse('blade ovate to depressed-ovate, round, '
                            'or flabellate, 2.5-15 × 2-10(-20) mm,'),
            [Trait(start=0, end=75, part='blade',
                   low_length=2.5, high_length=15,
                   low_width=2, high_width=10, max_width=20)])

    def test_parse_21(self):
        self.assertEqual(
            LEAF_SIZE.parse('blade broadly cordate to broadly ovate, ± as '
                            'long as wide, 1.2-6.5(-8.5) × 1.4-7(-8.2) cm'),
            [Trait(start=0, end=89, part='blade',
                   low_length=12, high_length=65, max_length=85,
                   low_width=14, high_width=70, max_width=82)])

    def test_parse_22(self):
        self.assertEqual(
            LEAF_SIZE.parse('blade pentagonal-angulate to reniform-angulate '
                            'or shallowly 5-angulate, sinuses 1/4–1/3 to '
                            'base, (3–)4–7 × 5–9 cm'),
            [Trait(start=0, end=113, part='blade',
                   min_length=30, low_length=40, high_length=70,
                   low_width=50, high_width=90)])

    def test_parse_23(self):
        self.maxDiff = None
        self.assertEqual(
            PETAL_SIZE.parse('petals (1–)3–10(–12) mm (pistillate) '
                             'or 5–8(–10) mm (staminate)'),
            [Trait(start=0, end=63, part='petals', sex='pistillate',
                   min_length=1, low_length=3, high_length=10, max_length=12),
             Trait(start=0, end=63, part='petals', sex='staminate',
                   low_length=5, high_length=8, max_length=10)])

    def test_parse_24(self):
        self.maxDiff = None
        self.assertEqual(
            LEAF_SIZE.parse('blade hastate to 5-angular, palmately '
                            '3–5-lobed, 3–8(–15) × 2–6(–8) cm,'),
            [Trait(start=0, end=70, part='blade',
                   low_length=30, high_length=80, max_length=150,
                   low_width=20, high_width=60, max_width=80)])

    def test_parse_25(self):
        self.maxDiff = None
        self.assertEqual(
            SEPAL_SIZE.parse('sepals (pistillate) linear, 6–7 mm;'),
            [Trait(start=0, end=34, part='sepals', sex='pistillate',
                   low_length=6, high_length=7)])

    def test_parse_26(self):
        self.maxDiff = None
        self.assertEqual(
            LEAF_SIZE.parse('blade suborbiculate to depressed-ovate, '
                            'palmately 5-lobed, sinuses 1/2–2/3 to petiole, '
                            '3–7 × 4–10 cm, usually broader than long '),
            [Trait(start=0, end=100, part='blade',
                   low_length=30, high_length=70,
                   low_width=40, high_width=100)])

    def test_parse_27(self):
        self.maxDiff = None
        self.assertEqual(
            PETIOLE_SIZE.parse('Leaves: petiole 1.5-7.5 (-12) cm'),
            [Trait(start=8, end=32, part='petiole',
                   low_length=15, high_length=75, max_length=120)])

    def test_parse_28(self):
        self.assertEqual(
            FLOWER_SIZE.parse('Flowers 5–10 cm diam.; hypanthium 4–8 mm,'),
            [Trait(start=0, end=20, dimension='diam', part='flowers',
                   low_length=50, high_length=100)])

    def test_parse_29(self):
        self.assertEqual(
            HYPANTHIUM_SIZE.parse('hypanthium cupulate, 5–8 mm;'),
            [Trait(start=0, end=27, part='hypanthium',
                   low_length=5, high_length=8)])
