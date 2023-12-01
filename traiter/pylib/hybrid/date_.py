from typing import Any

from .base import Base


class Date(Base):
    date = "dwc:eventDate"
    verbatim = "dwc:verbatimEventDate"
    match_verb = Base.case(verbatim)
    match = Base.case(
        date, "dwc:collectionDate dwc:earliestDateCollected dwc:latestDateCollected"
    )

    def __init__(self):
        super().__init__(self.event_date)

    def event_date(
        self, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, str]:
        t_val = traiter.get(self.date)
        o_val = self.search(other, self.match)

        if t_val and not o_val:
            raise ValueError(f"MISSING in OpenAI output {self.date} = {t_val}")

        if not o_val:
            return {}

        if not t_val or t_val == o_val or o_val in t_val:
            reconciled = {self.date: o_val}
            if verb := self.search(other, self.match_verb, traiter.get(self.verbatim)):
                reconciled[self.verbatim] = verb
            return reconciled

        if o_val == traiter.get(self.verbatim):
            return {
                self.date: traiter[self.date],
                self.verbatim: traiter[self.verbatim],
            }

        if t_val != o_val:
            raise ValueError(f"MISMATCH {self.date}: {o_val} != {t_val}")

        raise ValueError(f"UNKNOWN error in {self.date}")
