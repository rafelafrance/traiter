from typing import Any

from .base import Base


class DecimalLongitude(Base):
    label = "dwc:decimalLongitude"
    aliases = Base.case(label, "dwc:longitude dwc:verbatimLongitude")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, str]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        return {}
