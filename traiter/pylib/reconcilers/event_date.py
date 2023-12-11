from calendar import IllegalMonthError
from typing import Any

from dateutil import parser

from .. import darwin_core as dwc
from .base import Base


class EventDate(Base):
    label = "dwc:eventDate"
    verbatim_label = "dwc:verbatimEventDate"
    aliases = Base.get_aliases(
        """
        dwc:collectionDate dwc:earliestDateCollected dwc:latestDateCollected
        dwc:date"""
    )
    verbatim_aliases = Base.get_aliases(verbatim_label)

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, Any]:
        t_val = traiter.get(cls.label)
        o_val = cls.search(other, cls.aliases)
        t_verbatim = traiter.get(cls.verbatim_label)
        o_verbatim = cls.search(other, cls.verbatim_aliases)

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
                return {cls.label: dwc.SEP.join(o_val)}

        # Traiter found an event date but GPT did not
        if not o_val and t_val:
            # Does it match any other date?
            if cls.wildcard(other, "date"):
                return {}
            raise ValueError(f"MISSING in OpenAI output {cls.label} = {t_val}")

        # Neither found an event date
        if not o_val:
            return {}

        # GPT found a date, and it matches a date in traiter or traiter did not find one
        if not t_val or o_val == t_val or o_val in t_val:
            obj = {cls.label: o_val}
            if o_verbatim:
                obj[cls.verbatim_label] = o_verbatim
            elif t_verbatim:
                obj[cls.verbatim_label] = t_verbatim
            return obj

        # GPT's date matches Traiter's verbatim date. Use traiter's version
        if o_val == t_val:
            return {
                cls.label: t_val,
                cls.verbatim_label: t_verbatim,
            }

        # Try converting the OpenAI date
        if o_val != t_val:
            try:
                new = parser.parse(o_val).date().isoformat()[:10]
            except (parser.ParserError, IllegalMonthError):
                raise ValueError(f"MISMATCH {cls.label}: {o_val} != {t_val}")

            if new in t_val:
                return {
                    cls.label: t_val,
                    cls.verbatim_label: t_verbatim,
                }

            raise ValueError(f"MISMATCH {cls.label}: {o_val} != {t_val}")

        raise ValueError(f"UNKNOWN error in {cls.label}")
