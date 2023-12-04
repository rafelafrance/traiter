from calendar import IllegalMonthError
from typing import Any

from dateutil import parser

from .. import darwin_core as dwc
from .base import Base


class Date(Base):
    date_lb = "dwc:eventDate"
    verb_lb = "dwc:verbatimEventDate"
    match_verb = Base.case(verb_lb)
    match = Base.case(
        date_lb,
        "dwc:collectionDate dwc:earliestDateCollected dwc:latestDateCollected dwc:date",
    )

    def __init__(self):
        super().__init__(self.reconcile)

    def reconcile(
        self, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, str]:
        t_val = traiter.get(self.date_lb)
        o_val = self.search(other, self.match)

        # If OpenAI returns a dict see if we can use it
        if o_val and isinstance(o_val, dict):
            sub_keys = list(o_val.keys())
            if all(k in sub_keys for k in ("year", "month", "day")):
                new = f"{o_val['year']}-{o_val['month']}-{o_val['day']}"
                try:
                    new = parser.parse(new).date().isoformat()[:10]
                    o_val = new
                except (parser.ParserError, IllegalMonthError):
                    raise ValueError(f"BAD FORMAT in OpenAI output {o_val}")
            else:
                raise ValueError(f"BAD FORMAT in OpenAI output {o_val}")

        # Handle when OpenAI returns a list of dates
        if o_val and isinstance(o_val, list) and t_val:
            if any(v in t_val for v in o_val):
                return {self.date_lb: dwc.SEP.join(o_val)}

        # Traiter found an event date but GPT did not
        if not o_val and t_val:
            # Does it match any other date?
            if self.wildcard(other, "date"):
                return {}
            raise ValueError(f"MISSING in OpenAI output {self.date_lb} = {t_val}")

        # Neither found an event date
        if not o_val:
            return {}

        # GPT found a date, and it matches a date in traiter or traiter did not find one
        if not t_val or o_val == t_val or o_val in t_val:
            obj = {self.date_lb: o_val}
            if v := self.search(other, self.match_verb, traiter.get(self.verb_lb)):
                obj[self.verb_lb] = v
            return obj

        # GPT's date matches Traiter's verbatim date. Use traiter's version
        if o_val == traiter.get(self.verb_lb):
            return {
                self.date_lb: traiter[self.date_lb],
                self.verb_lb: traiter[self.verb_lb],
            }

        # Try converting the OpenAI date
        if o_val != t_val:
            try:
                new = parser.parse(o_val).date().isoformat()[:10]
            except (parser.ParserError, IllegalMonthError):
                raise ValueError(f"MISMATCH {self.date_lb}: {o_val} != {t_val}")

            if new in t_val:
                return {
                    self.date_lb: traiter[self.date_lb],
                    self.verb_lb: traiter[self.verb_lb],
                }

            raise ValueError(f"MISMATCH {self.date_lb}: {o_val} != {t_val}")

        raise ValueError(f"UNKNOWN error in {self.date_lb}")
