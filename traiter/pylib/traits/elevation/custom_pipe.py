import re
from dataclasses import dataclass

from spacy import Language

from ..base_custom_pipe import BaseCustomPipe
from traiter.pylib import util

CUSTOM_PIPE = "elevation_custom_pipe"


@Language.factory(CUSTOM_PIPE)
@dataclass()
class ElevationPipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]
    units_replace: dict[str, str]
    units_labels: list[str]
    factors_m: dict[str, float]
    dash: list[str]

    def __call__(self, doc):
        float_re = r"^(\d[\d,.]+)$"
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            values = []
            units = ""
            expected_len = 1

            for token in ent:
                # Find numbers
                if re.match(float_re, token.text) and len(values) < expected_len:
                    values.append(util.to_positive_float(token.text))

                # Find units
                elif token._.term in self.units_labels and not units:
                    units = self.units_replace.get(token.lower_, token.lower_)

                # If there's a dash it's a range
                elif token.text in self.dash:
                    expected_len = 2

            factor = self.factors_m[units]
            ent._.data["elevation"] = round(values[0] * factor, 3)

            # Handle a elevation range
            if expected_len == 2:
                ent._.data["elevation_high"] = round(values[1] * factor, 3)

        return doc
