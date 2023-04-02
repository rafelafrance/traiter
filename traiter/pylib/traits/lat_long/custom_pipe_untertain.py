import re
from dataclasses import dataclass

from spacy import Language

from traiter.pylib import util
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe
from traiter.pylib.traits.lat_long.pattern_compilers import FLOAT_RE

CUSTOM_PIPE_UNCERTAIN = "lat_long_uncertain_custom_pipe"


@Language.factory(CUSTOM_PIPE_UNCERTAIN)
@dataclass()
class LatLongPipeUncertain(BaseCustomPipe):
    id: str
    replace: dict[str, str]
    factors_m: dict[str, float]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.id_ == self.id]:
            units = ""
            value = 0.0
            for token in ent:
                # Get the data from the original parse
                if token._.data:
                    ent._.data = token._.data

                # Already parse
                elif token._.flag:
                    continue

                # Get the uncertainty units
                elif token._.term in ["metric_length", "imperial_length"]:
                    units = self.replace.get(token.lower_, token.lower_)

                # Get the uncertainty value
                elif re.match(FLOAT_RE, token.text):
                    value = util.to_positive_float(token.text)

            # Convert the values to meters
            ent._.data["units"] = "m"
            factor = self.factors_m[units]
            ent._.data["uncertainty"] = round(value * factor, 3)

        return doc
