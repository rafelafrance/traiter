import unittest
from lib.numeric_trait import NumericTrait
from lib.trait_builders.hind_foot_length_trait_builder \
    import HindFootLengthTraitBuilder


PAR = None


class TestHindFootLengthTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = HindFootLengthTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('hind foot with claw=30 mm;'),
            [NumericTrait(
                value=30, units='mm', includes='claw', start=0, end=25)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('"hindfootLengthInMM":"36"'),
            [NumericTrait(value=36, units='mm', start=1, end=24)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('"hind foot length":"34.0"'),
            [NumericTrait(value=34, units_inferred=True, start=1, end=24)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('; HindFoot: 30.0; '),
            [NumericTrait(value=30, units_inferred=True, start=2, end=16)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('{"measurements":"192-84-31-19=38g" }'),
            [NumericTrait(
                value=31, units='mm_shorthand', is_shorthand=True,
                start=2, end=33)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('{"measurements":"192-84-[31]-19=38g" }'),
            [NumericTrait(
                value=31, units='mm_shorthand', is_shorthand=True,
                estimated_value=True, start=2, end=35)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('T: 98.5, HF: 29 ;'),
            [NumericTrait(value=29, units_inferred=True, start=9, end=15)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('T-94mm, HF-30mm, E/n-19mm,'),
            [NumericTrait(value=30, units='mm', start=8, end=15)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('{"measurements":"210-92-30" }'),
            [NumericTrait(
                value=30, units='mm_shorthand', is_shorthand=True,
                start=2, end=26)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('measurements:210-92-30 308-190-45-20'),
            [NumericTrait(
                value=45, units='mm_shorthand', is_shorthand=True,
                start=23, end=36)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('measurements:210-92-30 185-252 mm'),
            [])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('"footLengthInMillimeters"="31",'),
            [NumericTrait(value=31, units='millimeters', start=1, end=29)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('{"measurements":"242-109-37-34=N/D" }'),
            [NumericTrait(
                value=37, units='mm_shorthand', is_shorthand=True,
                start=2, end=34)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('; hind foot with claw=2 in;'),
            [NumericTrait(
                value=50.8, units='in', includes='claw', start=2, end=26)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"eeba8b10-040e-4477-a0a6-870102b56234;'
                'abbf14f5-1a7c-48f6-8f2f-2a8af53c8c86"}'),
            [])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse(
                '{"created": "2007-05-27", "relatedresourceid": '
                '"92bc5a20-577e-4504-aab6-bb409d06871a;'
                '0460ccc4-a461-43ec-86b6-1c252377b126"}'),
            [])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"57d3efd8-2b9c-4952-8976-e27401a01251;'
                '8a35be5e-27fb-4875-81f6-42a5d7787760"}'),
            [])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse(
                '2010:15,27,41,69,106-107.112-115,118-128;'),
            [])
