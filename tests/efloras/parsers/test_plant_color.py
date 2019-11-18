import unittest
from pylib.efloras.trait import Trait
from pylib.efloras.parsers.plant_color import HYPANTHIUM_COLOR, COROLLA_COLOR
from pylib.efloras.parsers.plant_color import PETAL_COLOR, SEPAL_COLOR


class TestPlantColor(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            HYPANTHIUM_COLOR.parse(
                'hypanthium green or greenish yellow, '
                'usually not purple-spotted, rarely purple-spotted distally'),
            [Trait(start=0, end=86, part='hypanthium',
                   value=['green', 'green-yellow', 'purple-spotted'],
                   raw_value='green or greenish yellow, usually not '
                             'purple-spotted, rarely purple-spotted')])

    def test_parse_02(self):
        self.assertEqual(
            COROLLA_COLOR.parse('corolla yellow to orange-yellow,'),
            [Trait(start=0, end=31, value=['yellow', 'orange-yellow'],
                   part='corolla', raw_value='yellow to orange-yellow')])

    def test_parse_03(self):
        self.assertEqual(
            PETAL_COLOR.parse(
                'petals 5, connate 1/2-2/3 length, white, cream, '
                'or pale green [orange to yellow], '),
            [Trait(start=0, end=79, part='petals',
                   value=['white', 'green', 'orange', 'yellow'],
                   raw_value='white, cream, or pale green '
                             '[orange to yellow')])

    def test_parse_04(self):
        self.assertEqual(
            SEPAL_COLOR.parse('sepals erect, green- or red-tipped'),
            [Trait(start=0, end=34, part='sepals',
                   value=['green', 'red-tipped'],
                   raw_value='green- or red-tipped')])

    def test_parse_05(self):
        self.assertEqual(
            PETAL_COLOR.parse(
                'petals 5, distinct, white to cream, obovate to '
                'oblong-obovate, (15–)20–greenish yellow, maturing '
                'yellowish or pale brown, commonly mottled or with '
                'light green or white longitudinal stripes'),
            [Trait(start=0, end=188, part='petals',
                   value=['white', 'green-yellow', 'yellow', 'brown',
                          'green', 'white-longitudinal-stripes'],
                   raw_value=(
                       'white to cream, obovate to oblong-obovate, '
                       '(15–)20–greenish yellow, maturing yellowish or '
                       'pale brown, commonly mottled or with light green '
                       'or white longitudinal stripes'))])

    def test_parse_06(self):
        self.maxDiff = None
        self.assertEqual(
            PETAL_COLOR.parse(
                'petals 5, distinct, white to cream, greenish white, '
                'or yellowish green, or yellowish, usually green-throated '
                'and faintly green-lined,'),
            [Trait(start=0, end=132, part='petals',
                   value=['white', 'green-white', 'yellow-green', 'yellow',
                          'green-throated', 'green-lined'],
                   raw_value='white to cream, greenish '
                             'white, or yellowish green, or yellowish, '
                             'usually green-throated and faintly '
                             'green-lined')])
