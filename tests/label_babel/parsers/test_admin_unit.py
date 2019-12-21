# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods

import unittest
from pylib.shared.trait import Trait
from pylib.label_babel.parsers.admin_unit import ADMIN_UNIT


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
                   start=9, end=37)])

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
