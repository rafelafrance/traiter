import unittest

from tests.setup import to_ent
from traiter.pylib.darwin_core import DarwinCore

LABEL = "utm"


class TestUTM(unittest.TestCase):
    def test_utm_dwc_01(self):
        dwc = DarwinCore()
        verb = "UTM: 12s 359602E 3718689N"
        ent = to_ent(LABEL, verb)
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {"dynamicProperties": {"verbatimUTM": verb}},
        )
