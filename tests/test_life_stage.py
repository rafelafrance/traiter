# pylint: disable=missing-docstring,import-error,too-many-public-methods

from argparse import Namespace
import unittest
from lib.trait_parsers.life_stage import ParseLifeStage


class TestLifeStageParser(unittest.TestCase):

    def test_life_stage_key_value_delimited_01(self):
        self.assertDictEqual(
            TARGET.parse(['sex=unknown ; age class=adult/juvenile']),
            {'key': 'age class',
             'field': 'col1',
             'start': 14,
             'end': 38,
             'regex': 'life_stage_key_value_delimited',
             'value': 'adult/juvenile'})

    def test_life_stage_key_value_delimited_02(self):
        self.assertDictEqual(
            TARGET.parse(['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'key': 'age',
             'field': 'col1',
             'start': 31,
             'end': 40,
             'regex': 'life_stage_key_value_delimited',
             'value': 'u ad.'})

    def test_life_stage_key_value_delimited_03(self):
        self.assertDictEqual(
            TARGET.parse([
                'weight=5.2 g; age class=over-winter ; total length=99 mm;0']),
            {'key': 'age class',
             'field': 'col1',
             'start': 14,
             'end': 37,
             'regex': 'life_stage_key_value_delimited',
             'value': 'over-winter'})

    def test_life_stage_key_value_undelimited_01(self):
        self.assertDictEqual(
            TARGET.parse([
                'sex=female ? ; age=1st year more than four words here']),
            {'key': 'age',
             'field': 'col1',
             'start': 15,
             'end': 27,
             'regex': 'life_stage_key_value_undelimited',
             'value': '1st year'})

    def test_life_stage_no_keyword_01(self):
        self.assertDictEqual(
            TARGET.parse(['words after hatching year more words']),
            {'key': None,
             'field': 'col1',
             'start': 6,
             'end': 25,
             'regex': 'life_stage_no_keyword',
             'value': 'after hatching year'})

    def test_excluded_01(self):
        self.assertEqual(
            TARGET.parse(['age determined by 20-sided die']),
            None)

    def test_life_stage_no_keyword_02(self):
        self.assertDictEqual(
            TARGET.parse(['LifeStage Remarks: 5-6 wks']),
            {'key': 'LifeStage Remarks',
             'field': 'col1',
             'start': 0,
             'end': 26,
             'regex': 'life_stage_key_value_delimited',
             'value': '5-6 wks'})

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_01(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['sex=unknown ; age class=adult/juvenile']),
            {'derived_life_stage': 'adult/juvenile',
             'key': 'age class',
             'field': 'col1',
             'start': 14,
             'end': 38,
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_02(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'derived_life_stage': 'u ad.',
             'key': 'age',
             'regex': 'life_stage_key_value_delimited',
             'field': 'col1',
             'start': 31,
             'end': 40,
             'has_life_stage': True})

    def test_preferred_or_search_03(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['weight=5.2 g; age class=over-winter ; total length=99 mm;']),
            {'derived_life_stage': 'over-winter',
             'key': 'age class',
             'field': 'col1',
             'start': 14,
             'end': 37,
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_04(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['sex=female ? ; age=1st year more than four words here']),
            {'derived_life_stage': '1st year',
             'key': 'age',
             'field': 'col1',
             'start': 15,
             'end': 27,
             'regex': 'life_stage_key_value_undelimited',
             'has_life_stage': True})

    def test_preferred_or_search_05(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['', 'words after hatching year more words']),
            {'derived_life_stage': 'after hatching year',
             'key': None,
             'field': 'col2',
             'start': 6,
             'end': 25,
             'regex': 'life_stage_no_keyword',
             'has_life_stage': True})

    def test_preferred_or_search_06(self):
        self.assertEqual(
            TARGET.keyword_search(['age determined by 20-sided die']),
            {'derived_life_stage': '',
             'key': None,
             'field': None,
             'start': None,
             'end': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_07(self):
        self.assertDictEqual(
            TARGET.keyword_search(['LifeStage Remarks: 5-6 wks']),
            {'derived_life_stage': '5-6 wks',
             'key': 'LifeStage Remarks',
             'field': 'col1',
             'start': 0,
             'end': 26,
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_08(self):
        self.assertDictEqual(
            TARGET.keyword_search(['mentions juvenile']),
            {'derived_life_stage': 'juvenile',
             'field': 'col1',
             'start': 9,
             'end': 17,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_09(self):
        self.assertDictEqual(
            TARGET.keyword_search(
                ['mentions juveniles in the field']),
            {'derived_life_stage': 'juveniles',
             'key': None,
             'field': 'col1',
             'start': 9,
             'end': 18,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_10(self):
        self.assertDictEqual(
            TARGET.keyword_search(['one or more adults']),
            {'derived_life_stage': 'adults',
             'field': 'col1',
             'start': 12,
             'end': 18,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_11(self):
        self.assertDictEqual(
            TARGET.keyword_search(['adults']),
            {'derived_life_stage': 'adults',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 6,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_12(self):
        self.assertDictEqual(
            TARGET.keyword_search(['adult']),
            {'derived_life_stage': 'adult',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 5,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_13(self):
        self.assertDictEqual(
            TARGET.keyword_search(['Adulte']),
            {'derived_life_stage': 'Adulte',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 6,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_14(self):
        self.assertDictEqual(
            TARGET.keyword_search(['AGE IMM']),
            {'derived_life_stage': 'IMM',
             'key': 'AGE',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_15(self):
        self.assertDictEqual(
            TARGET.keyword_search(['subadult']),
            {'derived_life_stage': 'subadult',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 8,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_16(self):
        self.assertDictEqual(
            TARGET.keyword_search(['subadults']),
            {'derived_life_stage': 'subadults',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 9,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_17(self):
        self.assertDictEqual(
            TARGET.keyword_search(['subadultery']),
            {'derived_life_stage': '',
             'key': None,
             'field': None,
             'start': None,
             'end': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_18(self):
        self.assertDictEqual(
            TARGET.keyword_search(['in which larvae are found']),
            {'derived_life_stage': 'larvae',
             'key': None,
             'field': 'col1',
             'start': 9,
             'end': 15,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_19(self):
        self.assertDictEqual(
            TARGET.keyword_search(['larval']),
            {'derived_life_stage': 'larval',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 6,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_20(self):
        self.assertDictEqual(
            TARGET.keyword_search(['solitary larva, lonely']),
            {'derived_life_stage': 'larva',
             'key': None,
             'field': 'col1',
             'start': 9,
             'end': 14,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_21(self):
        self.assertDictEqual(
            TARGET.keyword_search(['juvénile']),
            {'derived_life_stage': 'juvénile',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 8,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_22(self):
        self.assertDictEqual(
            TARGET.keyword_search(['Têtard']),
            {'derived_life_stage': 'Têtard',
             'key': None,
             'field': 'col1',
             'start': 0,
             'end': 6,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_23(self):
        self.assertDictEqual(
            TARGET.keyword_search(['what if it is a subad.?']),
            {'derived_life_stage': 'subad',
             'key': None,
             'field': 'col1',
             'start': 16,
             'end': 21,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_24(self):
        self.assertDictEqual(
            TARGET.keyword_search(['subad is a possibility']),
            {'derived_life_stage': 'subad',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_25(self):
        self.assertDictEqual(
            TARGET.keyword_search(['one tadpole']),
            {'derived_life_stage': 'tadpole',
             'field': 'col1',
             'start': 4,
             'end': 11,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_26(self):
        self.assertDictEqual(
            TARGET.keyword_search(['two tadpoles']),
            {'derived_life_stage': 'tadpoles',
             'field': 'col1',
             'start': 4,
             'end': 12,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_27(self):
        self.assertDictEqual(
            TARGET.keyword_search(['an ad.']),
            {'derived_life_stage': 'ad',
             'field': 'col1',
             'start': 3,
             'end': 5,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_28(self):
        self.assertDictEqual(
            TARGET.keyword_search(['what about ad']),
            {'derived_life_stage': 'ad',
             'field': 'col1',
             'start': 11,
             'end': 13,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_29(self):
        self.assertDictEqual(
            TARGET.keyword_search(['ad. is a possibility']),
            {'derived_life_stage': 'ad',
             'field': 'col1',
             'start': 0,
             'end': 2,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_30(self):
        self.assertDictEqual(
            TARGET.keyword_search(['ad is also a possibility']),
            {'derived_life_stage': 'ad',
             'field': 'col1',
             'start': 0,
             'end': 2,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_31(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.keyword_search(['some embryos']),
            {'derived_life_stage': '',
             'field': None,
             'start': None,
             'end': None,
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_32(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.keyword_search(['an embryo']),
            {'derived_life_stage': '',
             'field': None,
             'start': None,
             'end': None,
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_33(self):
        self.assertDictEqual(
            TARGET.keyword_search(['embryonic']),
            {'derived_life_stage': '',
             'field': None,
             'start': None,
             'end': None,
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_34(self):
        self.assertDictEqual(
            TARGET.keyword_search(['IMM']),
            {'derived_life_stage': 'IMM',
             'field': 'col1',
             'start': 0,
             'end': 3,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_35(self):
        self.assertDictEqual(
            TARGET.keyword_search(['immature']),
            {'derived_life_stage': 'immature',
             'field': 'col1',
             'start': 0,
             'end': 8,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_36(self):
        self.assertDictEqual(
            TARGET.keyword_search(['immatures']),
            {'derived_life_stage': 'immatures',
             'field': 'col1',
             'start': 0,
             'end': 9,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_37(self):
        self.assertDictEqual(
            TARGET.keyword_search(['imm.']),
            {'derived_life_stage': 'imm',
             'field': 'col1',
             'start': 0,
             'end': 3,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_38(self):
        self.assertDictEqual(
            TARGET.keyword_search(['juv.']),
            {'derived_life_stage': 'juv',
             'field': 'col1',
             'start': 0,
             'end': 3,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_39(self):
        self.assertDictEqual(
            TARGET.keyword_search(['one juv to rule them all']),
            {'derived_life_stage': 'juv',
             'field': 'col1',
             'start': 4,
             'end': 7,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_40(self):
        self.assertDictEqual(
            TARGET.keyword_search(['how many juvs does it take?']),
            {'derived_life_stage': 'juvs',
             'field': 'col1',
             'start': 9,
             'end': 13,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_41(self):
        self.assertDictEqual(
            TARGET.keyword_search(['juvs.?']),
            {'derived_life_stage': 'juvs',
             'field': 'col1',
             'start': 0,
             'end': 4,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_42(self):
        self.assertDictEqual(
            TARGET.keyword_search(['juvenile(s)']),
            {'derived_life_stage': 'juvenile',
             'field': 'col1',
             'start': 0,
             'end': 8,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_43(self):
        self.assertDictEqual(
            TARGET.keyword_search(['larva(e)']),
            {'derived_life_stage': 'larva',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_44(self):
        self.assertDictEqual(
            TARGET.keyword_search(['young']),
            {'derived_life_stage': 'young',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_45(self):
        self.assertDictEqual(
            TARGET.keyword_search(['young adult']),
            {'derived_life_stage': 'young adult',
             'field': 'col1',
             'start': 0,
             'end': 11,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_46(self):
        self.assertDictEqual(
            TARGET.keyword_search(['adult young']),
            {'derived_life_stage': 'adult',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_47(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.keyword_search(['fetus']),
            {'derived_life_stage': '',
             'field': None,
             'start': None,
             'end': None,
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_48(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.keyword_search(['fetuses']),
            {'derived_life_stage': '',
             'field': None,
             'start': None,
             'end': None,
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_49(self):
        self.assertDictEqual(
            TARGET.keyword_search(['sub-adult']),
            {'derived_life_stage': 'sub-adult',
             'field': 'col1',
             'start': 0,
             'end': 9,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_50(self):
        self.assertDictEqual(
            TARGET.keyword_search(['hatched']),
            {'derived_life_stage': 'hatched',
             'field': 'col1',
             'start': 0,
             'end': 7,
             'regex': 'life_stage_unkeyed',
             'key': None,
             'has_life_stage': True})

    def test_preferred_or_search_51(self):
        self.assertDictEqual(
            TARGET.keyword_search(['adult(s) and juvenile(s)']),
            {'derived_life_stage': 'adult',
             'field': 'col1',
             'start': 0,
             'end': 5,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_52(self):
        self.assertDictEqual(
            TARGET.keyword_search(['juvenile(s) and adult(s)']),
            {'derived_life_stage': 'juvenile',
             'field': 'col1',
             'start': 0,
             'end': 8,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_53(self):
        self.assertDictEqual(
            TARGET.keyword_search(['young-of-the-year']),
            {'derived_life_stage': 'young-of-the-year',
             'field': 'col1',
             'start': 0,
             'end': 17,
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_54(self):
        self.assertDictEqual(
            TARGET.keyword_search(['YOLK SAC']),
            {'derived_life_stage': 'YOLK SAC',
             'field': 'col1',
             'start': 0,
             'end': 8,
             'key': None,
             'regex': 'life_stage_yolk_sac',
             'has_life_stage': True})


ARGS = Namespace(columns=['col1', 'col2', 'col3'])
TARGET = ParseLifeStage(ARGS)
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestLifeStageParser)
unittest.TextTestRunner().run(SUITE)
