import unittest

from tests.setup import to_ent

LABEL = "habitat"


class TestHabitat(unittest.TestCase):
    def test_habitat_dwc_01(self):
        ent = to_ent(LABEL, "subalpine zone")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(dwc.to_dict(), {"dwc:habitat": "subalpine zone"})
