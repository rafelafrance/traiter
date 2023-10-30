import unittest

from tests.setup import to_ent

LABEL = "trs"


class TestTRS(unittest.TestCase):
    def test_trs_dwc_01(self):
        ent = to_ent(LABEL, "TRS: NE/14 NW1/4 NW1/4 Nw1/4 S21 T39S R20E")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {"dwc:dynamicProperties": {"TRSPresent": "present"}},
        )
