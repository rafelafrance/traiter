# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods

import textwrap
import unittest
from traiter_shared.trait import Trait
from traiter_label_babel.parsers.admin_unit import ADMIN_UNIT


class TestAdminUnit(unittest.TestCase):

    def test_parse_01(self):
        """It gets a county notation."""
        self.assertEqual(
            ADMIN_UNIT.parse('Hempstead County'),
            [Trait(us_county='Hempstead', start=0, end=16)])

    def test_parse_02(self):
        """A label is required."""
        self.assertEqual(
            ADMIN_UNIT.parse('Watauga'),
            [])

    def test_parse_03(self):
        """It handles a confusing county notation."""
        self.assertEqual(
            ADMIN_UNIT.parse('Flora of ARKANSAS County: MISSISSIPPI'),
            [Trait(us_county='Mississippi', us_state='Arkansas',
                   start=0, end=37)])

    def test_parse_04(self):
        """It handles line breaks."""
        self.assertEqual(
            ADMIN_UNIT.parse('COUNTY:\n\nLee E.L.Nielsen'),
            [])

    def test_parse_05(self):
        """It handles a trailing county abbreviation."""
        self.assertEqual(
            ADMIN_UNIT.parse('Alleghany Co,'),
            [Trait(us_county='Alleghany', start=0, end=12)])

    def test_parse_06(self):
        """It normalizes state abbreviations."""
        self.assertEqual(
            ADMIN_UNIT.parse('Desha Co., Ark.'),
            [Trait(us_county='Desha', us_state='Arkansas', start=0, end=14)])

    def test_parse_07(self):
        """It works with noisy text."""
        self.assertEqual(
            ADMIN_UNIT.parse(textwrap.dedent("""
                Cornus drummondii C. A. Mey.
                Hempstead County
                Grandview Prairie; on CR 35, 10 air miles S/SE of Nashville; in
            """)),
            [Trait(us_county='Hempstead', start=30, end=46)])

    def test_parse_08(self):
        """It picks up common OCR errors."""
        self.assertEqual(
            ADMIN_UNIT.parse("""Caldwell Councy"""),
            [Trait(us_county='Caldwell', start=0, end=15)])

    def test_parse_09(self):
        """It gets a state notation."""
        self.assertEqual(
            ADMIN_UNIT.parse("""PLANTS OF ARKANSAS"""),
            [Trait(us_state='Arkansas', start=0, end=18)])

    def test_parse_10(self):
        """It gets a multi word state notation."""
        self.assertEqual(
            ADMIN_UNIT.parse("""PLANTS OF NORTH CAROLINA"""),
            [Trait(us_state='North Carolina', start=0, end=24)])

    def test_parse_11(self):
        """It gets a state notation separated from the county."""
        self.assertEqual(
            ADMIN_UNIT.parse(textwrap.dedent("""
                APPALACHIAN STATE UNIVERSITY HERBARIUM
                PLANTS OF NORTH CAROLINA
                STONE MOUNTAIN STATE PARK
                WILKES COUNTY
                """)),
            [Trait(us_state='North Carolina', start=40, end=64),
             Trait(us_county='Wilkes', start=91, end=104)])

    def test_parse_12(self):
        """It parses multiword counties and states."""
        self.assertEqual(
            ADMIN_UNIT.parse("""Cape May, New Jersey"""),
            [Trait(us_state='New Jersey', us_county='Cape May',
                   start=0, end=20)])

    def test_parse_13(self):
        """It find the correct parses."""
        self.assertEqual(
            ADMIN_UNIT.parse("""Cape May, New Jersey"""),
            [Trait(us_state='New Jersey', us_county='Cape May',
                   start=0, end=20)])

    def test_parse_14(self):
        """It normalizes the state."""
        self.assertEqual(
            ADMIN_UNIT.parse("St. Francis Co., AR TON RUE SE SE Survey #500"),
            [Trait(us_state='Arkansas', us_county='St. Francis',
                   start=0, end=19)])

    def test_parse_15(self):
        """It handles a eol between the state label and state."""
        self.assertEqual(
            ADMIN_UNIT.parse(textwrap.dedent("""
                PLANTS OF
                North Carolina
                """)),
            [Trait(us_state='North Carolina', start=1, end=25)])
