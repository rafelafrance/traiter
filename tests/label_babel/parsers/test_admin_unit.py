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
            [Trait(us_county='MISSISSIPPI', start=9, end=37)])
