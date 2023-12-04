from typing import Any

from .base import Base


class Habitat(Base):
    habitat_lb = "dwc:habitat"
    match = Base.case(habitat_lb)

    def __init__(self):
        super().__init__(self.reconcile)

    def reconcile(self, _: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
        o_val = self.search(other, self.match)

        obj = {}

        # Just use whatever is in the OpenAI output
        if o_val:
            obj[self.habitat_lb] = o_val

        return obj
