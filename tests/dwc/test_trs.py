import unittest

from tests.setup import to_ent
from traiter.pylib.darwin_core import DarwinCore

LABEL = "trs"


class TestTRS(unittest.TestCase):
    def test_trs_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "TRS: NE/14 NW1/4 NW1/4 Nw1/4 S21 T39S R20E")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {"dynamicProperties": {"TRSPresent": "present"}},
        )
