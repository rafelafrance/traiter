import unittest

from tests.setup import to_ent
from traiter.pylib.darwin_core import DarwinCore

LABEL = "color"


class TestColor(unittest.TestCase):
    def test_color_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "green")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"color": "green"}})

    def test_color_dwc_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "not purple-spotted")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"missingColor": "purple-spotted"}}
        )
