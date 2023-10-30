import unittest

from tests.setup import to_ent

LABEL = "elevation"


class TestElevation(unittest.TestCase):
    def test_elevation_dwc_01(self):
        ent = to_ent(LABEL, "Elev: 782m. (2566 ft)")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:verbatimElevation": "Elev: 782m. (2566 ft)",
                "dwc:minimumElevationInMeters": 782.0,
            },
        )

    def test_elevation_dwc_02(self):
        ent = to_ent(LABEL, "Elev. ca. 460 - 470 m")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:verbatimElevation": "Elev. ca. 460 - 470 m",
                "dwc:minimumElevationInMeters": 460.0,
                "dwc:maximumElevationInMeters": 470.0,
                "dwc:dynamicProperties": {"elevationUncertain": "uncertain"},
            },
        )
