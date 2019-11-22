import unittest
from pylib.stacked_regex.parser import scan
from pylib.stacked_regex.token import Token
from pylib.efloras.shared_plant import RULE


class TestSharedPlant(unittest.TestCase):

    def test_number_01(self):
        actual = scan([RULE['number']], '123')
        expect = [Token(
            RULE['number'], span=(0, 3), groups={'number': '123'})]
        self.assertEqual(actual, expect)

    def test_number_02(self):
        actual = scan([RULE['number']], '12.3')
        expect = [Token(
            RULE['number'], span=(0, 4), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_03(self):
        actual = scan([RULE['number']], '   12.3 x')
        expect = [Token(
            RULE['number'], span=(3, 7), groups={'number': '12.3'})]
        self.assertEqual(actual, expect)

    def test_number_04(self):
        actual = scan([RULE['number']], '12.3 4')
        expect = [
            Token(RULE['number'], span=(0, 4), groups={'number': '12.3'}),
            Token(RULE['number'], span=(5, 6), groups={'number': '4'})]
        self.assertEqual(actual, expect)

    def test_range_01(self):
        actual = scan([RULE['range']], '123')
        expect = [Token(RULE['range'], span=(0, 3),
                        groups={'range': '123', 'low': '123'})]
        self.assertEqual(actual, expect)

    def test_range_02(self):
        actual = scan([RULE['range']], '123-45')
        expect = [Token(
            RULE['range'], span=(0, 6),
            groups={'range': '123-45', 'low': '123', 'high': '45'})]
        self.assertEqual(actual, expect)

    def test_range_03(self):
        actual = scan([RULE['range']], '(12-)23-34(-45)')
        expect = [Token(
            RULE['range'], span=(0, 15),
            groups={'range': '(12-)23-34(-45)', 'low': '23', 'high': '34',
                    'min': '12', 'max': '45'})]
        self.assertEqual(actual, expect)

    def test_range_04(self):
        actual = scan([RULE['range']], '23-34(-45)')
        expect = [Token(
            RULE['range'], span=(0, 10),
            groups={'range': '23-34(-45)', 'low': '23', 'high': '34',
                    'max': '45'})]
        self.assertEqual(actual, expect)

    def test_range_05(self):
        actual = scan([RULE['range']], '(12-)23-34')
        expect = [Token(
            RULE['range'], span=(0, 10),
            groups={'range': '(12-)23-34', 'low': '23', 'high': '34',
                    'min': '12'})]
        self.assertEqual(actual, expect)

    def test_cross_01(self):
        actual = scan([RULE['cross']], '(12-)23-34')
        expect = [Token(
            RULE['cross'], span=(0, 10),
            groups={'cross': '(12-)23-34', 'length': '(12-)23-34',
                    'min_length': '12', 'low_length': '23',
                    'high_length': '34'})]
        self.assertEqual(actual, expect)

    def test_cross_02(self):
        actual = scan([RULE['cross']], '(12-)23-34 × 45-56')
        expect = [Token(
            RULE['cross'], span=(0, 18),
            groups={'cross': '(12-)23-34 × 45-56', 'length': '(12-)23-34',
                    'min_length': '12', 'low_length': '23',
                    'high_length': '34', 'width': '45-56',
                    'low_width': '45', 'high_width': '56'})]
        self.assertEqual(actual, expect)

    def test_upper_only_01(self):
        actual = scan([RULE['cross_upper']], 'to 10 cm')
        expect = [Token(
            RULE['cross_upper'], span=(0, 8),
            groups={'cross_upper': 'to 10 cm', 'high_length_upper': '10',
                    'units_length_upper': 'cm'})]
        self.assertEqual(actual, expect)
