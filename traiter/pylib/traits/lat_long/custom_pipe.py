import re
from dataclasses import dataclass

from spacy import Language

from traiter.pylib import util
from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe
from traiter.pylib.traits.lat_long.pattern_compilers import FLOAT_RE
from traiter.pylib.traits.lat_long.pattern_compilers import PUNCT

CUSTOM_PIPE = "lat_long_custom_pipe"
CUSTOM_PIPE_UNCERTAIN = "lat_long_uncertain_custom_pipe"


@Language.factory(CUSTOM_PIPE)
@dataclass()
class LatLongPipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            frags = []
            for token in ent:
                token._.flag = "lat_long"
                if token._.term == "lat_long_label":
                    continue
                if token._.term == "datum":
                    datum = self.replace.get(token.lower_, token.text)
                    ent._.data["datum"] = datum
                else:
                    text = token.text.upper() if len(token.text) == 1 else token.text
                    frags.append(text)

            lat_long = " ".join(frags)
            lat_long = re.sub(rf"\s([{PUNCT}])", r"\1", lat_long)
            lat_long = re.sub(rf"(-)\s", r"\1", lat_long)
            ent._.data[self.trait] = lat_long

            ent[0]._.data = ent._.data  # Save for uncertainty in the lat/long
        return doc


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
            factor = self.factors_m[units]

            ent._.data["uncertainty"] = round(value * factor, 3)
        return doc
