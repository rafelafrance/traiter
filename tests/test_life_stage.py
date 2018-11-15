# pylint: disable=missing-docstring,import-error,too-many-public-methods

import unittest
from lib.trait_parsers.life_stage import ParseLifeStage


class TestLifeStageParser(unittest.TestCase):

    def test_life_stage_key_value_delimited_01(self):
        self.assertDictEqual(
            TARGET.parse('sex=unknown ; age class=adult/juvenile'),
            {'key': 'age class',
             'regex': 'life_stage_key_value_delimited',
             'value': 'adult/juvenile'})

    def test_life_stage_key_value_delimited_02(self):
        self.assertDictEqual(
            TARGET.parse('weight=81.00 g; sex=female ? ; age=u ad.'),
            {'key': 'age',
             'regex': 'life_stage_key_value_delimited',
             'value': 'u ad.'})

    def test_life_stage_key_value_delimited_03(self):
        self.assertDictEqual(
            TARGET.parse(
                'weight=5.2 g; age class=over-winter ; total length=99 mm;'),
            {'key': 'age class',
             'regex': 'life_stage_key_value_delimited',
             'value': 'over-winter'})

    def test_life_stage_key_value_undelimited_01(self):
        self.assertDictEqual(
            TARGET.parse(
                'sex=female ? ; age=1st year more than four words here'),
            {'key': 'age',
             'regex': 'life_stage_key_value_undelimited',
             'value': '1st year'})

    def test_life_stage_no_keyword_01(self):
        self.assertDictEqual(
            TARGET.parse('words after hatching year more words'),
            {'key': None,
             'regex': 'life_stage_no_keyword',
             'value': 'after hatching year'})

    def test_excluded_01(self):
        self.assertEqual(
            TARGET.parse('age determined by 20-sided die'),
            None)

    def test_life_stage_no_keyword_02(self):
        self.assertDictEqual(
            TARGET.parse('LifeStage Remarks: 5-6 wks'),
            {'key': 'LifeStage Remarks',
             'regex': 'life_stage_key_value_delimited',
             'value': '5-6 wks'})

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################

    def test_preferred_or_search_01(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                ['sex=unknown ; age class=adult/juvenile']),
            {'derived_life_stage': 'adult/juvenile',
             'key': 'age class',
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_02(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                ['weight=81.00 g; sex=female ? ; age=u ad.']),
            {'derived_life_stage': 'u ad.',
             'key': 'age',
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_03(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                ['weight=5.2 g; age class=over-winter ; total length=99 mm;']),
            {'derived_life_stage': 'over-winter',
             'key': 'age class',
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_04(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                ['sex=female ? ; age=1st year more than four words here']),
            {'derived_life_stage': '1st year',
             'key': 'age',
             'regex': 'life_stage_key_value_undelimited',
             'has_life_stage': True})

    def test_preferred_or_search_05(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                ['words after hatching year more words']),
            {'derived_life_stage': 'after hatching year',
             'key': None,
             'regex': 'life_stage_no_keyword',
             'has_life_stage': True})

    def test_preferred_or_search_06(self):
        self.assertEqual(
            TARGET.preferred_or_search(['age determined by 20-sided die']),
            {'derived_life_stage': '',
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_07(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['LifeStage Remarks: 5-6 wks']),
            {'derived_life_stage': '5-6 wks',
             'key': 'LifeStage Remarks',
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_08(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['mentions juvenile']),
            {'derived_life_stage': 'juvenile',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_09(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(
                ['mentions juveniles in the field']),
            {'derived_life_stage': 'juveniles',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_10(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['one or more adults']),
            {'derived_life_stage': 'adults',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_11(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['adults']),
            {'derived_life_stage': 'adults',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_12(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['adult']),
            {'derived_life_stage': 'adult',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_13(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['Adulte']),
            {'derived_life_stage': 'Adulte',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_14(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['AGE IMM']),
            {'derived_life_stage': 'IMM',
             'key': 'AGE',
             'regex': 'life_stage_key_value_delimited',
             'has_life_stage': True})

    def test_preferred_or_search_15(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['subadult']),
            {'derived_life_stage': 'subadult',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_16(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['subadults']),
            {'derived_life_stage': 'subadults',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_17(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['subadultery']),
            {'derived_life_stage': '',
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_18(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['in which larvae are found']),
            {'derived_life_stage': 'larvae',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_19(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['larval']),
            {'derived_life_stage': 'larval',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_20(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['solitary larva, lonely']),
            {'derived_life_stage': 'larva',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_21(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['juvénile']),
            {'derived_life_stage': 'juvénile',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_22(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['Têtard']),
            {'derived_life_stage': 'Têtard',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_23(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['what if it is a subad.?']),
            {'derived_life_stage': 'subad',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_24(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['subad is a possibility']),
            {'derived_life_stage': 'subad',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_25(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['one tadpole']),
            {'derived_life_stage': 'tadpole',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_26(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['two tadpoles']),
            {'derived_life_stage': 'tadpoles',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_27(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['an ad.']),
            {'derived_life_stage': 'ad',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_28(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['what about ad']),
            {'derived_life_stage': 'ad',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_29(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['ad. is a possibility']),
            {'derived_life_stage': 'ad',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_30(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['ad is also a possibility']),
            {'derived_life_stage': 'ad',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_31(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.preferred_or_search(['some embryos']),
            {'derived_life_stage': '',
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_32(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.preferred_or_search(['an embryo']),
            {'derived_life_stage': '',
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_33(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['embryonic']),
            {'derived_life_stage': '',
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_34(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['IMM']),
            {'derived_life_stage': 'IMM',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_35(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['immature']),
            {'derived_life_stage': 'immature',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_36(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['immatures']),
            {'derived_life_stage': 'immatures',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_37(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['imm.']),
            {'derived_life_stage': 'imm',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_38(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['juv.']),
            {'derived_life_stage': 'juv',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_39(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['one juv to rule them all']),
            {'derived_life_stage': 'juv',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_40(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['how many juvs does it take?']),
            {'derived_life_stage': 'juvs',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_41(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['juvs.?']),
            {'derived_life_stage': 'juvs',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_42(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['juvenile(s)']),
            {'derived_life_stage': 'juvenile',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_43(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['larva(e)']),
            {'derived_life_stage': 'larva',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_44(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['young']),
            {'derived_life_stage': 'young',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_45(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['young adult']),
            {'derived_life_stage': 'young',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_46(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['adult young']),
            {'derived_life_stage': 'adult',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_47(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.preferred_or_search(['fetus']),
            {'derived_life_stage': '',
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_48(self):
        # Lifestage removed
        self.assertDictEqual(
            TARGET.preferred_or_search(['fetuses']),
            {'derived_life_stage': '',
             'key': None,
             'regex': None,
             'has_life_stage': False})

    def test_preferred_or_search_49(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['sub-adult']),
            {'derived_life_stage': 'sub-adult',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_50(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['hatched']),
            {'derived_life_stage': 'hatched',
             'regex': 'life_stage_unkeyed',
             'key': None,
             'has_life_stage': True})

    def test_preferred_or_search_51(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['adult(s) and juvenile(s)']),
            {'derived_life_stage': 'adult',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_52(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['juvenile(s) and adult(s)']),
            {'derived_life_stage': 'juvenile',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_53(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['young-of-the-year']),
            {'derived_life_stage': 'young-of-the-year',
             'key': None,
             'regex': 'life_stage_unkeyed',
             'has_life_stage': True})

    def test_preferred_or_search_54(self):
        self.assertDictEqual(
            TARGET.preferred_or_search(['YOLK SAC']),
            {'derived_life_stage': 'YOLK SAC',
             'key': None,
             'regex': 'life_stage_yolk_sac',
             'has_life_stage': True})


TARGET = ParseLifeStage()
SUITE = unittest.defaultTestLoader.loadTestsFromTestCase(TestLifeStageParser)
unittest.TextTestRunner().run(SUITE)
