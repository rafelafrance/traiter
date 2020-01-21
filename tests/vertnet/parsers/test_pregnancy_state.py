# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods
import unittest
from traiter_vertnet.trait import Trait
from traiter_vertnet.parsers.pregnancy_state import PREGNANCY_STATE


class TestPregnancyState(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('pregnant; 4 emb 3L 1R'),
            [Trait(value='pregnant', start=0, end=8)])

    def test_parse_02(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('not pregnant; not lactating'),
            [Trait(value='not pregnant', start=0, end=12)])

    def test_parse_03(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('non-lactating, non-pregnant'),
            [Trait(value='non-pregnant', start=15, end=27)])

    def test_parse_04(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('Box ID: UAFWALR34. Recent Pregnancy.'),
            [Trait(value='recent pregnancy', start=19, end=35)])

    def test_parse_05(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('probably pregnant'),
            [Trait(value='probably pregnant', start=0, end=17)])

    def test_parse_06(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('Fox was pregnant, but'),
            [Trait(value='was pregnant', start=4, end=16)])

    def test_parse_07(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('GMU catalog.  Pregnant?'),
            [Trait(value='pregnant?', start=14, end=23)])

    def test_parse_08(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('IMPREGNATED WITH POLYVINYL ACETATE'),
            [])

    def test_parse_09(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('probably early pregnancy'),
            [Trait(value='probably early pregnancy', start=0, end=24)])

    def test_parse_10(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('No NK# assigned previously, pregnant'),
            [Trait(value='pregnant', start=28, end=36)])

    def test_parse_11(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('possible early pregnancy'),
            [Trait(value='possible early pregnancy', start=0, end=24)])

    def test_parse_12(self):
        self.assertEqual(
            PREGNANCY_STATE.parse(',prob. pregnant,'),
            [Trait(value='prob. pregnant', start=1, end=15)])

    def test_parse_13(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('; not visibly pregnant,'),
            [Trait(value='not visibly pregnant', start=2, end=22)])

    def test_parse_14(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('No evidence of pregnancy,'),
            [Trait(value='no evidence of pregnancy', start=0, end=24)])

    def test_parse_15(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('males and a pregnant female,'),
            [Trait(value='pregnant', start=12, end=20)])

    def test_parse_16(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('pregnancy not evident'),
            [Trait(value='pregnancy not evident', start=0, end=21)])

    def test_parse_17(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('*Two pregnancies were visible on uterus.'),
            [Trait(value='pregnancies were visible', start=5, end=29)])

    def test_parse_18(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('number 2859; female; no pregnancies'),
            [Trait(value='no pregnancies', start=21, end=35)])

    def test_parse_19(self):
        self.assertEqual(
            PREGNANCY_STATE.parse('reproductive data=Not gravid'),
            [Trait(value='not gravid', start=18, end=28)])
