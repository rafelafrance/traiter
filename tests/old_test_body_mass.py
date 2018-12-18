# pylint: disable=missing-docstring,import-error,too-many-public-methods

from argparse import Namespace
import unittest
from lib.trait_parsers.body_mass import ParseBodyMass


class TestBodyMassParser(unittest.TestCase):

    def test_01(self):
        self.assertDictEqual(
            TARGET.parse(['762-292-121-76 2435.0g']),
            {'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 22,
             'value': '2435.0',
             'units': 'g'})

    def test_02(self):
        self.assertDictEqual(
            TARGET.parse(['TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx']),
            {'key': 'Weight',
             'regex': 'wt_key_word',
             'field': 'col1',
             'start': 22,
             'end': 37,
             'value': '0.77',
             'units': 'g'})

    def test_03(self):
        self.assertDictEqual(
            TARGET.parse([
                'Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g']),
            {'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 41,
             'end': 55,
             'value': '62',
             'units': 'g'})

    def test_04(self):
        self.assertDictEqual(
            TARGET.parse(['body mass=20 g']),
            {'key': 'body mass',
             'regex': 'total_wt_key',
             'field': 'col1',
             'start': 0,
             'end': 14,
             'value': '20',
             'units': 'g'})

    def test_05(self):
        self.assertDictEqual(
            TARGET.parse(['2 lbs. 3.1 - 4.5 oz ']),
            {'key': '_english_',
             'regex': 'en_wt',
             'field': 'col1',
             'start': 0,
             'end': 19,
             'value': ['2', '3.1 - 4.5'],
             'units': ['lbs.', 'oz']})

    def test_06(self):
        self.assertDictEqual(
            TARGET.parse([
                '{"totalLengthInMM":"x", "earLengthInMM":"20", '
                '"weight":"[139.5] g" }']),
            {'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 47,
             'end': 65,
             'value': '[139.5]',
             'units': 'g'})

    def test_07(self):
        self.assertDictEqual(
            TARGET.parse([
                '{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", '
                '"molt":"No molt", '
                '"stomach contents":"Not recorded", "weight":"94 gr."']),
            {'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 101,
             'end': 116,
             'value': '94',
             'units': 'gr.'})

    def test_08(self):
        self.assertDictEqual(
            TARGET.parse(['Note in catalog: 83-0-17-23-fa64-35g']),
            {'key': '_shorthand_',
             'regex': 'wt_fa',
             'field': 'col1',
             'start': 28,
             'end': 36,
             'value': '35',
             'units': 'g'})

    def test_09(self):
        self.assertDictEqual(
            TARGET.parse(['{"measurements":"20.2g, SVL 89.13mm" }']),
            {'key': 'measurements',
             'regex': 'key_units_req',
             'field': 'col1',
             'start': 2,
             'end': 22,
             'value': '20.2',
             'units': 'g'})

    def test_10(self):
        self.assertDictEqual(
            TARGET.parse(['Body: 15 g']),
            {'key': 'Body',
             'regex': 'key_units_req',
             'field': 'col1',
             'start': 0,
             'end': 10,
             'value': '15',
             'units': 'g'})

    def test_11(self):
        self.assertDictEqual(
            TARGET.parse(['82-00-15-21-tr7-fa63-41g']),
            {'key': '_shorthand_',
             'regex': 'wt_fa',
             'field': 'col1',
             'start': 16,
             'end': 24,
             'value': '41',
             'units': 'g'})

    def test_12(self):
        self.assertDictEqual(
            TARGET.parse(
                ['weight=5.4 g; unformatted measurements=77-30-7-12=5.4']),
            {'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 0,
             'end': 12,
             'value': '5.4',
             'units': 'g'})

    def test_13(self):
        self.assertDictEqual(
            TARGET.parse(
                ['unformatted measurements=77-30-7-12=5.4; weight=5.4;']),
            {'key': 'measurements',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 12,
             'end': 39,
             'value': '5.4',
             'units': None})

    def test_14(self):
        self.assertDictEqual(
            TARGET.parse(['{"totalLengthInMM":"270-165-18-22-31", ']),
            {'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 20,
             'end': 36,
             'value': '31',
             'units': None})

    def test_15(self):
        self.assertDictEqual(
            TARGET.parse(['{"measurements":"143-63-20-17=13 g" }']),
            {'key': 'measurements',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 34,
             'value': '13',
             'units': 'g'})

    def test_16(self):
        self.assertDictEqual(
            TARGET.parse(['143-63-20-17=13']),
            {'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 15,
             'value': '13',
             'units': None})

    def test_17(self):
        self.assertDictEqual(
            TARGET.parse([
                'reproductive data: Testes descended -10x7 mm; sex: male;'
                ' unformatted measurements: 181-75-21-18=22 g']),
            {'key': 'measurements',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 69,
             'end': 100,
             'value': '22',
             'units': 'g'})

    def test_18(self):
        self.assertDictEqual(
            TARGET.parse(['{ "massingrams"="20.1" }']),
            {'key': 'massingrams',
             'regex': 'total_wt_key',
             'field': 'col1',
             'start': 3,
             'end': 21,
             'value': '20.1',
             'units': 'grams'})

    def test_19(self):
        self.assertDictEqual(
            TARGET.parse([
                ' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", '
                '"weight":"1,192.0" }']),
            {'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 54,
             'end': 70,
             'value': '1,192.0',
             'units': None})

    def test_20(self):
        self.assertDictEqual(
            TARGET.parse(['"weight: 20.5-31.8']),
            {'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 18,
             'value': '20.5-31.8',
             'units': None})

    def test_21(self):
        self.assertDictEqual(
            TARGET.parse(['"weight: 20.5-32']),
            {'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 16,
             'value': '20.5-32',
             'units': None})

    def test_22(self):
        self.assertDictEqual(
            TARGET.parse(['"weight: 21-31.8']),
            {'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 16,
             'value': '21-31.8',
             'units': None})

    def test_23(self):
        self.assertDictEqual(
            TARGET.parse(['"weight: 21-32']),
            {'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 14,
             'value': '21-32',
             'units': None})

    def test_24(self):
        self.assertEqual(
            TARGET.parse([
                "Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                "5507,5508,5590,"
                "5592,5595,5594,5593,5596,5589,5587,5586,5585"]),
            None)

    def test_25(self):
        self.assertDictEqual(
            TARGET.parse([
                'weight=5.4 g; unformatted measurements=77-x-7-12=5.4']),
            {'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 0,
             'end': 12,
             'value': '5.4',
             'units': 'g'})

    def test_26(self):
        self.assertEqual(
            TARGET.parse(['c701563b-dbd9-4500-184f-1ad61eb8da11']),
            None)

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_27(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['762-292-121-76 2435.0g']),
            {'found': True,
             'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 22,
             'grams': 2435.0,
             'units_inferred': False})

    def test_28(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['TL (mm) 44,SL (mm) 38,Weight (g) 0.77 xx']),
            {'found': True,
             'key': 'Weight',
             'regex': 'wt_key_word',
             'field': 'col1',
             'start': 22,
             'end': 37,
             'grams': 0.77,
             'units_inferred': False})

    def test_29(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['Note in catalog: Mus. SW Biol. NK 30009; 91-0-17-22-62g']),
            {'found': True,
             'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 41,
             'end': 55,
             'grams': 62,
             'units_inferred': False})

    def test_30(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['body mass=20 g']),
            {'found': True,
             'key': 'body mass',
             'regex': 'total_wt_key',
             'field': 'col1',
             'start': 0,
             'end': 14,
             'grams': 20,
             'units_inferred': False})

    def test_31(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['2 lbs. 3.1 - 4.5 oz ']),
            {'found': True,
             'key': '_english_',
             'regex': 'en_wt',
             'field': 'col1',
             'start': 0,
             'end': 19,
             'grams': [994.9, 1034.6],
             'units_inferred': False})

    def test_32(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"totalLengthInMM":"x", "earLengthInMM":"20", '
                 '"weight":"[139.5] g" }']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 47,
             'end': 65,
             'grams': 139.5,
             'units_inferred': False})

    def test_33(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"fat":"No fat", "gonads":"Testes 10 x 6 mm.", '
                 '"molt":"No molt",'
                 ' "stomach contents":"Not recorded", "weight":"94 gr."']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 101,
             'end': 116,
             'grams': 94,
             'units_inferred': False})

    def test_34(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['Note in catalog: 83-0-17-23-fa64-35g']),
            {'found': True,
             'key': '_shorthand_',
             'regex': 'wt_fa',
             'field': 'col1',
             'start': 28,
             'end': 36,
             'grams': 35,
             'units_inferred': False})

    def test_35(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"measurements":"20.2g, SVL 89.13mm" }']),
            {'found': True,
             'key': 'measurements',
             'regex': 'key_units_req',
             'field': 'col1',
             'start': 2,
             'end': 22,
             'grams': 20.2,
             'units_inferred': False})

    def test_36(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['Body: 15 g']),
            {'found': True,
             'key': 'Body',
             'regex': 'key_units_req',
             'field': 'col1',
             'start': 0,
             'end': 10,
             'grams': 15,
             'units_inferred': False})

    def test_37(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['82-00-15-21-tr7-fa63-41g']),
            {'found': True,
             'key': '_shorthand_',
             'regex': 'wt_fa',
             'field': 'col1',
             'start': 16,
             'end': 24,
             'grams': 41,
             'units_inferred': False})

    def test_38(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['weight=5.4 g; unformatted measurements=77-30-7-12=5.4']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 0,
             'end': 12,
             'grams': 5.4,
             'units_inferred': False})

    def test_39(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['unformatted measurements=77-30-7-12=5.4; weight=5.4;']),
            {'found': True,
             'key': 'measurements',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 12,
             'end': 39,
             'grams': 5.4,
             'units_inferred': True})

    def test_40(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"totalLengthInMM":"270-165-18-22-31", ']),
            {'found': True,
             'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 20,
             'end': 36,
             'grams': 31,
             'units_inferred': True})

    def test_41(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['{"measurements":"143-63-20-17=13 g" }']),
            {'found': True,
             'key': 'measurements',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 2,
             'end': 34,
             'grams': 13,
             'units_inferred': False})

    def test_42(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['143-63-20-17=13']),
            {'found': True,
             'key': '_shorthand_',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 0,
             'end': 15,
             'grams': 13,
             'units_inferred': True})

    def test_43(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['reproductive data: Testes descended -10x7 mm; sex: male;'
                 ' unformatted measurements: 181-75-21-18=22 g']),
            {'found': True,
             'key': 'measurements',
             'regex': 'wt_shorthand',
             'field': 'col1',
             'start': 69,
             'end': 100,
             'grams': 22,
             'units_inferred': False})

    def test_44(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['{ "massingrams"="20.1" }']),
            {'found': True,
             'key': 'massingrams',
             'regex': 'total_wt_key',
             'field': 'col1',
             'start': 3,
             'end': 21,
             'grams': 20.1,
             'units_inferred': False})

    def test_45(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                [' {"gonadLengthInMM_1":"10", "gonadLengthInMM_2":"6", '
                 '"weight":"1,192.0" }']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 54,
             'end': 70,
             'grams': 1192.0,
             'units_inferred': True})

    def test_46(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['"weight: 20.5-31.8']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 18,
             'grams': [20.5, 31.8],
             'units_inferred': True})

    def test_47(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['"weight: 20.5-32']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 16,
             'grams': [20.5, 32],
             'units_inferred': True})

    def test_48(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['"weight: 21-31.8']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 16,
             'grams': [21, 31.8],
             'units_inferred': True})

    def test_49(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['"weight: 21-32']),
            {'found': True,
             'key': 'weight',
             'regex': 'wt_key_ambiguous',
             'field': 'col1',
             'start': 1,
             'end': 14,
             'grams': [21, 32],
             'units_inferred': True})

    def test_50(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ["Specimen #'s - 5491,5492,5498,5499,5505,5526,5527,5528,5500,"
                 "5507,5508,5590,"
                 "5592,5595,5594,5593,5596,5589,5587,5586,5585"]),
            {'found': False,
             'key': None,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'grams': None,
             'units_inferred': False})

    def test_51(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(
                ['weight=5.4 g; unformatted measurements=77-x-7-12=5.4']),
            {'found': True,
             'grams': 5.4,
             'key': 'weight',
             'regex': 'wt_key_word_req',
             'field': 'col1',
             'start': 0,
             'end': 12,
             'units_inferred': False})

    def test_52(self):
        self.assertEqual(
            TARGET.search_and_normalize(
                ['c701563b-dbd9-4500-184f-1ad61eb8da11']),
            {'found': False,
             'grams': None,
             'key': None,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'units_inferred': False})

    def test_53(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['body mass=0 g']),
            {'found': False,
             'key': None,
             'regex': None,
             'field': None,
             'start': None,
             'end': None,
             'grams': None,
             'units_inferred': False})

    def test_54(self):
        self.assertDictEqual(
            TARGET.search_and_normalize(['2 lbs. 3.1 oz ']),
            {'found': True,
             'key': '_english_',
             'regex': 'en_wt',
             'field': 'col1',
             'start': 0,
             'end': 13,
             'grams': 994.9,
             'units_inferred': False})


ARGS = Namespace(columns=['col1', 'col2', 'col3'])
TARGET = ParseBodyMass(ARGS)
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestBodyMassParser)
unittest.TextTestRunner().run(SUITE)
