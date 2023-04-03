import re
from dataclasses import dataclass

from spacy import Language

from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe
from traiter.pylib.traits.lat_long.lat_long_pattern_compilers import PUNCT

LAT_LONG_CUSTOM_PIPE = "lat_long_custom_pipe"


@Language.factory(LAT_LONG_CUSTOM_PIPE)
@dataclass()
class LatLongPipe(BaseCustomPipe):
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "lat_long"]:
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
            ent._.data["lat_long"] = lat_long

            ent[0]._.data = ent._.data  # Save for uncertainty in the lat/long
        return doc
