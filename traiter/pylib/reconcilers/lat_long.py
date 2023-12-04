from typing import Any

from .. import darwin_core as dwc
from .base import Base


class LatLong(Base):
    lat_lb = "dwc:decimalLatitude"
    long_lb = "dwc:decimalLongitude"
    sys_lb = "dwc:verbatimCoordinateSystem"
    prec_lb = "dwc:coordinatePrecision"
    verb_lb = "dwc:verbatimCoordinates"
    uncert_lb = "dwc:coordinateUncertaintyInMeters"
    datum_lb = "dwc:geodeticDatum"

    match_lat = Base.case(lat_lb, "dwc:latitude dwc:verbatimLatitude")
    match_long = Base.case(lat_lb, "dwc:longitude dwc:verbatimLongitude")
    match_sys = Base.case(sys_lb, "dwc:coordinateSystem")
    match_prec = Base.case(prec_lb, "")
    match_verb = Base.case(verb_lb, "dwc:coordinates")
    match_uncert = Base.case(uncert_lb, "")
    match_datum = Base.case(datum_lb, "datum")

    def __init__(self):
        super().__init__(self.reconcile)

    def reconcile(
        self, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, str]:
        o_lat = self.search(other, self.match_lat)
        o_long = self.search(other, self.match_long)
        o_sys = self.search(other, self.match_sys)
        o_prec = self.search(other, self.match_prec)
        o_verb = self.search(other, self.match_verb)
        o_uncert = self.search(other, self.match_uncert)
        o_datum = self.search(other, self.match_datum)

        t_verb = traiter.get(self.verb_lb)
        t_datum = traiter.get(self.datum_lb)
        t_uncert = traiter.get(self.uncert_lb)

        obj = {}

        # Default to what's in the OpenAI output
        if o_lat:
            obj[self.lat_lb] = o_lat

        if o_long:
            obj[self.long_lb] = o_long

        if o_sys:
            obj[self.sys_lb] = o_sys

        if o_prec:
            obj[self.prec_lb] = o_prec

        if o_verb:
            obj[self.verb_lb] = o_verb
        elif t_verb:
            obj[self.verb_lb] = t_verb

        if isinstance(o_uncert, list):
            obj[self.uncert_lb] = dwc.SEP.join(o_uncert)
        elif o_uncert:
            obj[self.uncert_lb] = o_uncert
        elif t_uncert:
            obj[self.uncert_lb] = t_uncert

        if o_datum:
            obj[self.datum_lb] = o_datum
        elif t_datum:
            obj[self.datum_lb] = t_datum

        return obj
