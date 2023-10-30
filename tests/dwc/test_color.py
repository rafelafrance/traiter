import unittest

from tests.setup import to_ent

LABEL = "color"


class TestColor(unittest.TestCase):
    def test_color_dwc_01(self):
        ent = to_ent(LABEL, "green")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(dwc.to_dict(), {"dwc:dynamicProperties": {"color": "green"}})

    def test_color_dwc_02(self):
        ent = to_ent(LABEL, "not purple-spotted")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"missingColor": "purple-spotted"}}
        )
