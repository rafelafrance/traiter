import unittest
from datetime import date

from dateutil.relativedelta import relativedelta

from tests.setup import test


class TestDate(unittest.TestCase):
    def test_date_01(self):
        """It handles a date with a month name in the middle."""
        self.assertEqual(
            test("""11 May 2004"""),
            [
                {
                    "date": "2004-05-11",
                    "trait": "date",
                    "start": 0,
                    "end": 11,
                },
            ],
        )

    def test_date_02(self):
        """It handles a date with a month name in the middle and a 2-digit year."""
        self.assertEqual(
            test("11 may 04"),
            [
                {
                    "date": "2004-05-11",
                    "trait": "date",
                    "start": 0,
                    "end": 9,
                },
            ],
        )

    def test_date_03(self):
        """It adjusts future dates back a century for a 2-digit year."""
        tomorrow = date.today() + relativedelta(days=1)
        tomorrow = tomorrow.strftime("%d %b %y")
        expect = date.today() + relativedelta(years=-100, days=1)
        expect = expect.strftime("%Y-%m-%d")
        self.assertEqual(
            test(tomorrow),
            [
                {
                    "date": expect,
                    "century_adjust": True,
                    "trait": "date",
                    "start": 0,
                    "end": 9,
                },
            ],
        )

    def test_date_04(self):
        """It handles noise prior to parsing the date."""
        self.assertEqual(
            test("No.: 113,306 Date: 8 October 1989"),
            [
                {
                    "date": "1989-10-08",
                    "trait": "date",
                    "start": 13,
                    "end": 33,
                },
            ],
        )

    def test_date_05(self):
        """It handles an all numeric date."""
        self.assertEqual(
            test("11-0297 10/20/2011"),
            [
                {
                    "date": "2011-10-20",
                    "trait": "date",
                    "start": 8,
                    "end": 18,
                },
            ],
        )

    def test_date_06(self):
        """It handles noise in the separators."""
        self.assertEqual(
            test("Collected by D, M, MOORE — Date AUG-_11,1968"),
            [
                {
                    "date": "1968-08-11",
                    "trait": "date",
                    "start": 27,
                    "end": 44,
                },
            ],
        )

    def test_date_07(self):
        """It handles slashes between the date parts."""
        self.assertEqual(
            test("""Date 8/20/75"""),
            [
                {
                    "date": "1975-08-20",
                    "trait": "date",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_date_08(self):
        """It handles dates missing a day part (numeric)."""
        self.assertEqual(
            test("Andrew Jenkins 631 2/2010"),
            [
                {
                    "date": "2010-02",
                    "missing_day": True,
                    "trait": "date",
                    "start": 19,
                    "end": 25,
                },
            ],
        )

    def test_date_09(self):
        """It does not parse a bad date."""
        self.assertEqual(
            test("Date Oct. 6, 197"),
            [],
        )

    def test_date_10(self):
        """It handles a bad month."""
        self.assertEqual(
            test("May have elevation: 1347.22 m (4420 N) - 1359-40 m (4460 Ny"),
            [{"elevation": 1347.22, "end": 29, "start": 9, "trait": "elevation"}],
        )

    def test_date_11(self):
        """It handles a bad month."""
        self.assertEqual(
            test("June, 1992"),
            [
                {
                    "date": "1992-06",
                    "trait": "date",
                    "missing_day": True,
                    "start": 0,
                    "end": 10,
                },
            ],
        )

    def test_date_12(self):
        """It handles an abbreviated month."""
        self.assertEqual(
            test("14 Jan. 1987"),
            [
                {
                    "date": "1987-01-14",
                    "trait": "date",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_date_13(self):
        """It skips a list of numbers.."""
        self.assertEqual(
            test("2 8 10"),
            [],
        )

    def test_date_14(self):
        """It allows the 'yy notation."""
        self.assertEqual(
            test("Date: 6/30 '66"),
            [
                {
                    "century_adjust": True,
                    "date": "1966-06-30",
                    "trait": "date",
                    "start": 0,
                    "end": 14,
                }
            ],
        )

    def test_date_15(self):
        """It handles an abbreviated month."""
        self.assertEqual(
            test("14 jan. 1987"),
            [
                {
                    "date": "1987-01-14",
                    "trait": "date",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_date_16(self):
        """It handles an abbreviated month."""
        self.assertEqual(
            test("14 JAN. 1987"),
            [
                {
                    "date": "1987-01-14",
                    "trait": "date",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_date_17(self):
        """It handles month first."""
        self.assertEqual(
            test("W May 19, 1998 HR1998-01"),
            [
                {
                    "date": "1998-05-19",
                    "trait": "date",
                    "start": 2,
                    "end": 14,
                },
            ],
        )

    def test_date_18(self):
        self.assertEqual(
            test("5/26/03,"),
            [
                {
                    "date": "2003-05-26",
                    "trait": "date",
                    "start": 0,
                    "end": 7,
                },
            ],
        )
