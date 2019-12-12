import unittest
from pylib.stacked_regex.parser import Parser
from pylib.stacked_regex.token import Token
from pylib.stacked_regex.rule import producer
from pylib.shared.patterns import RULE


def nop(token):
    """Create a dummy function for tests."""
    return token


class TestSharedPatterns(unittest.TestCase):
    #     def test_cross_03(self):
    #         parser = Parser([RULE['cross_set'], self.cross_product])
    #         actual = parser.parse('9 12.3 x 45.6 8')
    #         expect = [
    #             Token(
    #                 rule=self.cross_product, span=(2, 13),
    #                 groups={'number': ['12.3', '45.6'], 'x': 'x',
    #                         'cross': '12.3 x 45.6',
    #                         'cross_product': '12.3 x 45.6'})]
    #         self.assertEqual(actual, expect)
    #
    #     def test_cross_04(self):
    #         parser = Parser([RULE['cross_set'], self.cross_product])
    #         actual = parser.parse('12x34x56')
    #         expect = [
    #             Token(
    #                 rule=self.cross_product, span=(0, 5),
    #                 groups={'number': ['12', '34'], 'x': 'x',
    #                         'cross': '12x34', 'cross_product': '12x34'})]
    #         self.assertEqual(actual, expect)
    #
    #     def test_cross_05(self):
    #         parser = Parser([RULE['cross_set'], self.cross_product])
    #         actual = parser.parse('3x1.5mm')
    #         expect = [Token(
    #             rule=self.cross_product, span=(0, 7),
    #             groups={'number': ['3', '1.5'], 'x': 'x',
    #                     'cross': '3x1.5mm', 'cross_product': '3x1.5mm',
    #                     'metric_len': 'mm', 'len_units': 'mm'})]
    #         self.assertEqual(actual, expect)
    #
    #     def test_cross_06(self):
    #         parser = Parser([RULE['cross_set'], self.cross_product])
    #         actual = parser.parse('3mmx1.5mm')
    #         expect = [Token(
    #             rule=self.cross_product, span=(0, 9),
    #             groups={
    #               'number': ['3', '1.5'], 'x': 'x',
    #               'cross': '3mmx1.5mm', 'cross_product': '3mmx1.5mm',
    #               'metric_len': ['mm', 'mm'], 'len_units': ['mm', 'mm']})]
    #         self.assertEqual(actual, expect)
    #
    #     def test_cross_07(self):
    #         parser = Parser([RULE['cross_set'], self.cross_product])
    #         actual = parser.parse('12.3mm')
    #         expect = [
    #             Token(
    #                 rule=self.cross_product, span=(0, 6),
    #                 groups={'number': '12.3',
    #                         'cross': '12.3mm', 'cross_product': '12.3mm',
    #                         'metric_len': 'mm', 'len_units': 'mm'})]
    #         self.assertEqual(actual, expect)
    #
    #     def test_fraction_01(self):
    #         parser = Parser([RULE['fraction_set'], self.fraction_product])
    #         actual = parser.parse('12/34')
    #         expect = [Token(
    #             rule=self.fraction_product, span=(0, 5),
    #             groups={'number': ['12', '34'], 'slash': '/',
    #                     'fraction': '12/34', 'fraction_product': '12/34'})]
    #         self.assertEqual(actual, expect)
    #
    #     def test_fraction_02(self):
    #         parser = Parser([RULE['fraction_set'], self.fraction_product])
    #         actual = parser.parse('12/34/56')
    #         expect = []
    #         self.assertEqual(actual, expect)

    def test_uuid_01(self):
        parser = Parser(RULE['uuid'])
        actual = parser.parse('ddf2d94a-0a49-11ea-a133-000000000004')
        expect = [Token(
            RULE['uuid'], span=(0, 36),
            groups={})]
        self.assertEqual(actual, expect)
