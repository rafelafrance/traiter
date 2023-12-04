from pathlib import Path
from typing import Any

from traiter.pylib import term_util, util

from .base import Base


class Elevation(Base):
    lo_lb = "dwc:minimumElevationInMeters"
    hi_lb = "dwc:maximumElevationInMeters"
    verb_lb = "dwc:verbatimElevation"
    match_verb = Base.case(verb_lb)
    match_lo = Base.case(
        lo_lb,
        """
        dwc:decimalElevation dwc:elevation dwc:elevationInMeters
        dwc:minElevationInMeters minimumElevationinMeters
        dwc:minElevationInFeet dwc:minimumElevationInFeet""",
    )
    match_hi = Base.case(
        hi_lb,
        """
        dwc:maxElevationInMeters dwc:maxElevationInFeet dwc:maximumElevationInFeet""",
    )

    term_dir = Path(__file__).parent / ".." / "rules" / "terms"
    unit_csv = term_dir / "unit_length_terms.csv"
    tic_csv = term_dir / "unit_tic_terms.csv"
    factors_cm = term_util.term_data((unit_csv, tic_csv), "factor_cm", float)
    factors_m = {k: v / 100.0 for k, v in factors_cm.items()}

    def __init__(self):
        super().__init__(self.reconcile)

    def reconcile(
        self, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, Any]:
        o_lo = self.search(other, self.match_lo)

        # Make sure what OpenAI returned is a string
        if o_lo and not isinstance(o_lo, (str, float, int)):
            raise ValueError(f"BAD FORMAT in OpenAI output {o_lo}")

        o_lo = util.to_positive_float(o_lo) if o_lo is not None else o_lo

        o_hi = self.search(other, self.match_hi)
        o_hi = util.to_positive_float(o_hi) if o_hi is not None else o_hi

        t_lo = traiter.get(self.lo_lb)
        # t_hi = traiter.get(self.lo_lb)

        # No match
        if not o_lo and not o_hi:
            return {}

        # A simple match
        if o_lo == t_lo and not o_hi:
            obj = {self.lo_lb: o_lo, self.verb_lb: traiter[self.verb_lb]}
            if o_hi:
                obj[self.hi_lb] = o_hi

        # Try matching on feet
        if o_lo and t_lo:
            factor = self.factors_m["ft"]
            ft_to_m = round(o_lo * factor, 3)
            if ft_to_m == t_lo:
                obj = {self.lo_lb: ft_to_m, self.verb_lb: traiter[self.verb_lb]}
                if o_hi:
                    ft_to_m = round(o_hi * factor, 3)
                    obj[self.hi_lb] = ft_to_m
                return obj

            raise ValueError(f"MISMATCH {self.lo_lb}: {o_lo} != {t_lo}")

        if o_lo and not t_lo:
            raise ValueError(f"NO TRAITER MATCH: {o_lo}")

        raise ValueError(f"UNKNOWN error in {self.lo_lb}")
