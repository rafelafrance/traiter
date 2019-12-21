# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods

from datetime import date
import unittest
from dateutil.relativedelta import relativedelta
from pylib.shared.trait import Trait
from pylib.label_babel.parsers.label_date import DATE


class TestLabelDate(unittest.TestCase):

    def test_parse_01(self):
        """It parses a date with a month name."""
        self.assertEqual(
            DATE.parse('11 May 2004'),
            [Trait(value='2004-05-11', start=0, end=11)])

    def test_parse_02(self):
        """It parses a date with a two digit year."""
        self.assertEqual(
            DATE.parse('11 may 04'),
            [Trait(value='2004-05-11', start=0, end=9)])

    def test_parse_03(self):
        """It adjusts future dates back a century."""
        tomorrow = date.today() + relativedelta(days=1)
        tomorrow = tomorrow.strftime('%d %b %y')
        expect = date.today() + relativedelta(years=-100, days=1)
        expect = expect.strftime('%Y-%m-%d')
        self.assertEqual(
            DATE.parse(tomorrow),
            [Trait(value=expect, century_adjust=True, start=0, end=9)])

    def test_parse_04(self):
        """It handles noise prior to parsing the date."""
        self.assertEqual(
            DATE.parse('No.: 113,306 Date: 8 October 1989'),
            [Trait(value='1989-10-08', start=13, end=33)])

    def test_parse_05(self):
        """It handles an all numeric date."""
        self.assertEqual(
            DATE.parse('Brent Baker 11-0297 10/20/2011'),
            [Trait(value='2011-10-20', start=20, end=30)])

    def test_parse_06(self):
        """It grabes the date label."""
        self.assertEqual(
            DATE.parse('Date June 6, 1973'),
            [Trait(value='1973-06-06', start=0, end=17)])

    def test_parse_07(self):
        """It handles dashes as a numeric separator."""
        self.assertEqual(
            DATE.parse('Date 8-14-77'),
            [Trait(value='1977-08-14', start=0, end=12)])

    def test_parse_09(self):
        """It handles no spaces between the date parts."""
        self.assertEqual(
            DATE.parse('11may04'),
            [Trait(value='2004-05-11', start=0, end=7)])
