from . import base


class Elevation(base.Base):
    keys = [
        "dwc:decimalElevation",
        "dwc:elevation",
        "dwc:elevationAccuracy",
        "dwc:elevationInMeters",
        "dwc:maxElevationInMeters",
        "dwc:maximumElevationInFeet",
        "dwc:maximumElevationInFeet",
        "dwc:maximumElevationInMeters",
        "dwc:minElevationInMeters",
        "dwc:minimumElevationInMeters",
        "dwc:verbatimElevation",
    ]

    def __init__(self):
        super().__init__(self.elevation)

    def elevation(self):
        ...
