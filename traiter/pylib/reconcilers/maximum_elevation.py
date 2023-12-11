from typing import Any

from traiter.pylib import util

from .base import Base


class MaximumElevationInMeters(Base):
    label = "dwc:maximumElevationInMeters"
    aliases = Base.get_aliases(
        label,
        """
        dwc:maxElevationInMeters dwc:maxElevationInFeet dwc:maximumElevationInFeet""",
    )

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, Any]:
        o_val = cls.search(other, cls.aliases)

        # Make sure what OpenAI returned is a string
        if o_val and not isinstance(o_val, (str, float, int)):
            raise ValueError(f"BAD FORMAT in OpenAI output {o_val}")

        o_val = util.to_positive_float(o_val) if o_val is not None else o_val
        t_val = traiter.get(cls.label)

        # No match
        if not t_val and not o_val:
            return {}

        # A simple match
        if o_val == t_val:
            return {cls.label: o_val}

        # Try matching on feet
        if o_val and t_val:
            factor = cls.factors_m["ft"]
            ft_to_m = round(o_val * factor, 3)
            if ft_to_m == t_val:
                return {cls.label: ft_to_m}

            raise ValueError(f"MISMATCH {cls.label}: {o_val} != {t_val}")

        if o_val and not t_val:
            raise ValueError(f"NO TRAITER MATCH: {cls.label} {o_val}")

        raise ValueError(f"UNKNOWN error in {cls.label}")
