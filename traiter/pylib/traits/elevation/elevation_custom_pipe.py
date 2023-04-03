import re
from dataclasses import dataclass

from spacy import Language

from ... import const
from ..base_custom_pipe import BaseCustomPipe
from traiter.pylib import util

ELEVATION_CUSTOM_PIPE = "elevation_custom_pipe"
UNITS = ("metric_length", "imperial_length")


@Language.factory(ELEVATION_CUSTOM_PIPE)
@dataclass()
class ElevationPipe(BaseCustomPipe):
    replace: dict[str, str]
    factors_m: dict[str, float]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "elevation"]:
            values = []
            units = ""
            expected_len = 1

            for token in ent:
                # Find numbers
                if re.match(const.FLOAT_RE, token.text) and len(values) < expected_len:
                    values.append(util.to_positive_float(token.text))

                # Find units
                elif token._.term in UNITS and not units:
                    units = self.replace.get(token.lower_, token.lower_)

                # If there's a dash it's a range
                elif token.text in const.DASH:
                    expected_len = 2

            ent._.data["units"] = "m"
            factor = self.factors_m[units]
            ent._.data["elevation"] = round(values[0] * factor, 3)

            # Handle a elevation range
            if expected_len == 2:
                ent._.data["elevation_high"] = round(values[1] * factor, 3)

        return doc
