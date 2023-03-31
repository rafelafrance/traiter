import re
from calendar import IllegalMonthError
from dataclasses import dataclass
from datetime import date

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy import Language

from ..base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE = "date_pipe"


@Language.factory(CUSTOM_PIPE)
@dataclass()
class DatePipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]
    sep: str

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            frags = []

            for token in ent:
                # Get the numeric parts
                if re.match(rf"^[\d{self.sep}]+$", token.text):
                    parts = [p for p in re.split(rf"[{self.sep}]+", token.text) if p]
                    if parts:
                        frags += parts

                # Get a month name
                elif token._.term == "month":
                    frags.append(self.replace.get(token.lower_, token.lower_))

            # Try to parse the date
            text = " ".join(frags)
            try:
                date_ = parser.parse(text).date()
            except (parser.ParserError, IllegalMonthError):
                ent._.delete = True
                return

            # Handle missing centuries like: May 22, 08
            if date_ > date.today():
                date_ -= relativedelta(years=100)
                ent._.data["century_adjust"] = True

            ent._.data[self.trait] = date_.isoformat()[:10]

            # If this is a date without a day then truncate the output
            if ent.id_ == "short_date":
                ent._.data["missing_day"] = True
                ent._.data[self.trait] = date_.isoformat()[:7]

        return doc
