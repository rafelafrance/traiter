import unittest

from tests.setup import to_ent

LABEL = "date"


class TestDate(unittest.TestCase):
    def test_date_dwc_01(self):
        ent = to_ent(LABEL, "14 JAN. 1987")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(dwc.to_dict(), {"dwc:eventDate": "1987-01-14"})
