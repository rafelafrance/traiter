import unittest
from lib.parse import Parse
from lib.traits.testes_state_trait import TestesStateTrait


PAR = TestesStateTrait()


class TestTestesStateTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('some words reproductive data=No testicles; more words'),
            [Parse(value='no testicles', start=11, end=41)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('testes descended'),
            [Parse(value='descended', start=0, end=16)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('testes undescended'),
            [Parse(value='undescended', start=0, end=18)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('testes undesc.'),
            [Parse(value='undesc', start=0, end=13)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('testes undesc'),
            [Parse(value='undesc', start=0, end=13)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('testes not fully descended'),
            [Parse(value='not fully descended', start=0, end=26)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('testes not-scrotal'),
            [Parse(value='not-scrotal', start=0, end=18)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('testes no scrotum'),
            [Parse(value='no scrotum', start=0, end=17)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('testis nscr'),
            [Parse(value='nscr', start=0, end=11)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('testes ns'),
            [Parse(value='ns', start=0, end=9)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('tes undescend.'),
            [Parse(value='undescend', start=0, end=13)])

    def test_parse_12(self):
        self.assertEqual(
            PAR.parse('t abdominal'),
            [Parse(value='abdominal', start=0, end=11)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('t nscr'),
            [Parse(value='nscr', start=0, end=6)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('t ns'),
            [])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse(
                ('hind foot with claw=35 mm; '
                 'reproductive data=Testes partially descended. '
                 'Sperm present.')),
            [Parse(value='partially descended', start=27, end=71)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse(
                ('sex=male ; reproductive data=testis 5mm, abdominal '
                 '; ear from notch=20 mm; ')),
            [Parse(value='abdominal', start=11, end=50)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse(('tag# 1089; bag# 156; no gonads')),
            [Parse(value='no gonads', ambiguous_key=True, start=21, end=30)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse(
                'weight=36 g; reproductive data=testes: 11x7 mm (scrotal)'),
            [Parse(value='scrotal', start=13, end=55)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse(
                ('non-scrotal, sem. ves. 14 mm ')),
            [Parse(value='non-scrotal', start=0, end=11)])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse(
                ('verbatim preservation date=8 October 1986 ; '
                 'reproductive data=No testicles')),
            [Parse(value='no testicles', start=44, end=74)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse(
                ('weight=53 g; reproductive data=testes decended, T=8x3 ;')),
            [Parse(value='decended', start=13, end=46)])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse(
                ('weight=75.6 g; reproductive data=Testes small')),
            [Parse(value='small', start=15, end=45)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse(
                ('weight=75.6 g; reproductive data=small')),
            [Parse(value='small', start=15, end=38)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('puncture wound in left abdominal region.'),
            [])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse(' reproductive data=plsc'),
            [])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse(
                ('junk before reproductive data=Testes small, not descended')),
            [Parse(value='small, not descended', start=12, end=57)])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('Mixed woods // TESTES NOT DESCENDED'),
            [Parse(value='not descended', start=15, end=35)])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse(
                ('reproductive data=Uteri small, clear')),
            [])

    def test_parse_29(self):
        self.assertEqual(
            PAR.parse(
                ('sex=male ; age class=adult ; reproductive data=scrotal ; '
                 'hind foot with claw=32 mm; weight=82 g; weight=78 g; '
                 'weight=87 g; weight=94 g; reproductive data=nonscrotal ; '
                 'sex=male ; sex=male ; reproductive data=nonscrotal ; '
                 'reproductive data=nonscrotal ; sex=male ; hind foot with '
                 'claw=32 mm; hind foot with claw=34 mm; hind foot with '
                 'claw=34 mm; age class=adult ; age class=adult ; '
                 'age class=adult')),
            [Parse(value='scrotal', start=29, end=54),
             Parse(value='nonscrotal', start=136, end=164),
             Parse(value='nonscrotal', start=189, end=217),
             Parse(value='nonscrotal', start=220, end=248)])

    def test_parse_30(self):
        self.assertEqual(
            PAR.parse('reproductive data=NS ;'),
            [Parse(value='ns', start=0, end=20)])

    def test_parse_31(self):
        self.assertEqual(
            PAR.parse('reproductive data=SCR ;'),
            [Parse(value='scr', start=0, end=21)])

    def test_parse_32(self):
        self.assertEqual(
            PAR.parse('; reproductive data=testes = 4x3 mm; '),
            [])

    def test_parse_33(self):
        self.assertEqual(
            PAR.parse('Deciduous woods // TESTES DESCENDED, AND ENLARGED'),
            [Parse(value='descended, and enlarged', start=19, end=49)])

    def test_parse_34(self):
        self.assertEqual(
            PAR.parse('Testis abd. Collected with 22 cal. pellet rifle.'),
            [Parse(value='abd', start=0, end=10)])

    def test_parse_35(self):
        # self.maxDiff = None
        self.assertEqual(
            PAR.parse('reproductive data=test 3.5x2, pt desc, Et not visib,'),
            [Parse(value='pt desc', start=0, end=37)])
