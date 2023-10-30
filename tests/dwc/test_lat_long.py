import unittest

from tests.setup import to_ent
from traiter.pylib.darwin_core import DarwinCore

LABEL = "lat_long"


class TestLatLong(unittest.TestCase):
    def test_lat_long_dwc_01(self):
        verb = "40.104905N, 79.324561W NAD83"
        ent = to_ent(LABEL, "floodplain wetland. " + verb)
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {"dwc:verbatimCoordinates": verb, "dwc:geodeticDatum": "NAD83"},
        )

    def test_lat_long_dwc_02(self):
        verb = "43.963272° N, 113.446226° W Uncertainty: 100 m."
        ent = to_ent(LABEL, verb)
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:verbatimCoordinates": verb,
                "dwc:coordinateUncertaintyInMeters": 100.0,
            },
        )
