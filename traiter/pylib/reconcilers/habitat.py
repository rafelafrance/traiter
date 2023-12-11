from typing import Any

from .base import Base


class Habitat(Base):
    label = "dwc:habitat"
    aliases = Base.case(label)

    @classmethod
    def reconcile(cls, _: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        return {}