# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring,too-many-public-methods

import textwrap
import unittest
from pylib.shared.trait import Trait
from pylib.label_babel.parsers.plant_taxon import PLANT_TAXON, PLANT_FAMILY


class TestPlantTaxon(unittest.TestCase):

    def test_parse_01(self):
        """It gets a taxon notation."""
        self.assertEqual(
            PLANT_TAXON.parse(textwrap.dedent("""
                Cornaceae
                Cornus obliqua Raf.
                Washington County""")),
            [Trait(value='Cornus obliqua Raf.', start=11, end=30)])

    def test_parse_02(self):
        """It gets a family notation."""
        self.assertEqual(
            PLANT_FAMILY.parse(textwrap.dedent("""
                Crowley's Ridge
                Fabaceae
                Vicia villosa Roth ssp. varia (Host) Corb.
                CLAY COUNTY
                """)),
            [Trait(value='Fabaceae', start=17, end=25)])
