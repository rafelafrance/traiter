from typing import Any

from .base import Base


class CoordinatePrecision(Base):
    label = "dwc:coordinatePrecision"
    aliases = Base.case(label)

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, str]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        return {}