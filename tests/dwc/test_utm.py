import unittest

from tests.setup import to_ent

LABEL = "utm"


class TestUTM(unittest.TestCase):
    def test_utm_dwc_01(self):
        verb = "UTM: 12s 359602E 3718689N"
        ent = to_ent(LABEL, verb)
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {"dwc:dynamicProperties": {"verbatimUTM": verb}},
        )
