import unittest
from pylib.vertnet.numeric_trait import NumericTrait
from pylib.vertnet.parsers.tail_length import TAIL_LENGTH


class TestTailLength(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            TAIL_LENGTH.parse('tailLengthInmm: 102'),
            [NumericTrait(
                value=102, units='mm', units_inferred=False, start=0, end=19)])

    def test_parse_02(self):
        self.assertEqual(
            TAIL_LENGTH.parse('tail length=95 mm;'),
            [NumericTrait(
                value=95, units='mm', units_inferred=False, start=0, end=17)])

    def test_parse_03(self):
        self.assertEqual(
            TAIL_LENGTH.parse('tail length=95;'),
            [NumericTrait(
                value=95, units=None, units_inferred=True, start=0, end=14)])

    def test_parse_04(self):
        self.assertEqual(
            TAIL_LENGTH.parse(', "tail":"92", '),
            [NumericTrait(
                value=92, units=None, units_inferred=True, start=3, end=12)])

    def test_parse_05(self):
        self.assertEqual(
            TAIL_LENGTH.parse('"tailLengthInMillimeters"="104",'),
            [NumericTrait(
                value=104, units='millimeters', units_inferred=False,
                start=1, end=30)])

    def test_parse_06(self):
        self.assertEqual(
            TAIL_LENGTH.parse('measurements:213-91-32-23'),
            [NumericTrait(
                value=91, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=0, end=25)])

    def test_parse_07(self):
        self.assertEqual(
            TAIL_LENGTH.parse('213-91-32-23'),
            [NumericTrait(
                value=91, units='mm_shorthand', units_inferred=False,
                is_shorthand=True, start=0, end=12)])

    def test_parse_08(self):
        self.assertEqual(
            TAIL_LENGTH.parse('taillength=95;'),
            [NumericTrait(
                value=95, units=None, units_inferred=True, start=0, end=13)])

    def test_parse_09(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                'reproductive data=testes abdominal; T = 3 x 1.8 ;'),
            [])

    def test_parse_10(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"eeba8b10-040e-4477-a0a6-870102b56234;'
                'abbf14f5-1a7c-48f6-8f2f-2a8af53c8c86"}'),
            [])

    def test_parse_11(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                '{"created": "2007-05-27", "relatedresourceid": '
                '"92bc5a20-577e-4504-aab6-bb409d06871a;'
                '0460ccc4-a461-43ec-86b6-1c252377b126"}'),
            [])

    def test_parse_12(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                '{"created": "2014-10-29", "relatedresourceid": '
                '"57d3efd8-2b9c-4952-8976-e27401a01251;'
                '8a35be5e-27fb-4875-81f6-42a5d7787760"}'),
            [])

    def test_parse_13(self):
        self.assertEqual(
            TAIL_LENGTH.parse('ELEV G.T. 3900 FT'), [])

    def test_parse_14(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                '"Dry muscle tissue accessioned into the Southwest Fisheries '
                'Science Center (SWFSC) collection, T_ID 178858, LABID '
                '144207. Recovered by Henry Swanson. Scheffer, V. B. (1949). '
                '"Notes of three beaked whales from the Aleutian Islands." '
                'Pacific Science 3(4):353."'),
            [])

    def test_parse_15(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                '95 on skull; [total: 773.5mm tail: 280.0 foot: 65.0 '
                'pina: 41.0; 24 June 1986]'),
            [NumericTrait(
                value=85344, units='foot', units_inferred=False,
                start=29, end=45)])

    def test_parse_16(self):
        self.assertEqual(
            TAIL_LENGTH.parse('Body and tail: 1690 mm; Body: 114000 g'),
            [])

    def test_parse_17(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                'Other Measurements: nose-tail=60in., girth=39in.'),
            [])

    def test_parse_18(self):
        self.assertEqual(
            TAIL_LENGTH.parse(
                'Imm. weight 50 kg, L. snout to tip of tail 1510,'),
            [])

    def test_parse_19(self):
        self.assertEqual(
            TAIL_LENGTH.parse('; trap identifier=CN02-T01/19 ;'),
            [])

    def test_parse_20(self):
        self.assertEqual(
            TAIL_LENGTH.parse('scrotal t.21mm'),
            [])
