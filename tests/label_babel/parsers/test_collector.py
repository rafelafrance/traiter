# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods

import unittest
from pylib.shared.trait import Trait
from pylib.label_babel.parsers.collector import COLLECTOR


class TestLabelDate(unittest.TestCase):

    def test_parse_01(self):
        """It parses a collector name & number."""
        self.assertEqual(
            COLLECTOR.parse('Coll. M. P. Locke No. 4823'),
            [Trait(col_name='M. P. Locke', col_no='4823', start=0, end=26)])

    def test_parse_02(self):
        """It parses a several collectors."""
        self.assertEqual(
            COLLECTOR.parse('Sarah Nunn and S. Jacobs and R. Mc Elderry 9480'),
            [
                Trait(col_name='Sarah Nunn', col_no='9480', start=0, end=47),
                Trait(col_name='S. Jacobs', start=0, end=47),
                Trait(col_name='R. Mc Elderry', start=0, end=47),
            ])

    def test_parse_03(self):
        """It does not parse other fields."""
        self.assertEqual(
            COLLECTOR.parse("""
            Rhus glabra L. "Smooth Sumac"
            Woodruff Co., Arkansas
            Vicinity of bridge on Hwy 33, ca. 2 mi. S. of the
            town of Gregory; S19, T6N; R3W.
            Det, Edwin B. Smith
            Coll. Marie P. Locke No. 5595
            Date June 29, 1985
            """),
            [Trait(col_name='Marie P. Locke', col_no='5595',
                   start=228, end=257)])

    def test_parse_04(self):
        """It handles a bad name."""
        self.assertEqual(
            COLLECTOR.parse("""
            APPALACHIAN STATE UNIVERSITY HERBARIUM
            PLANTS OF NORTH CAROLINA
            Collected by _Wayne.. Hutchins.
            """),
            [Trait(col_name='Hutchins',  start=101, end=131)])
