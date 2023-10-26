import unittest

from tests.setup import to_ent
from traiter.pylib.darwin_core import DarwinCore

LABEL = "elevation"


class TestElevation(unittest.TestCase):
    def test_elevation_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Elev: 782m. (2566 ft)")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "verbatimElevation": "Elev: 782m. (2566 ft)",
                "minimumElevationInMeters": 782.0,
            },
        )

    def test_elevation_dwc_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Elev. ca. 460 - 470 m")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "verbatimElevation": "Elev. ca. 460 - 470 m",
                "minimumElevationInMeters": 460.0,
                "maximumElevationInMeters": 470.0,
                "dynamicProperties": {"elevationUncertain": "uncertain"},
            },
        )
