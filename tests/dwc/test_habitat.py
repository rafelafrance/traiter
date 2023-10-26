import unittest

from tests.setup import to_ent
from traiter.pylib.darwin_core import DarwinCore

LABEL = "habitat"


class TestHabitat(unittest.TestCase):
    def test_habitat_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "subalpine zone")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"habitat": "subalpine zone"})
