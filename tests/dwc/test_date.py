import unittest

from tests.setup import to_ent
from traiter.pylib.darwin_core import DarwinCore

LABEL = "date"


class TestDate(unittest.TestCase):
    def test_date_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "14 JAN. 1987")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"eventDate": "1987-01-14"})
