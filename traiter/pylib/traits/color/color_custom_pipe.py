from dataclasses import dataclass

from spacy import Language

from ... import const
from ..base_custom_pipe import BaseCustomPipe

COLOR_CUSTOM_PIPE = "color_custom_pipe"


@Language.factory(COLOR_CUSTOM_PIPE)
@dataclass()
class ColorPipe(BaseCustomPipe):
    replace: dict[str, str]
    remove: dict[str, int]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "color"]:
            frags = []

            for token in ent:
                # Skip anything that is not a term
                if not token._.term:
                    continue

                # Skip terms marked for removal
                if self.remove.get(token.lower_):
                    continue

                # Skip names like "Brown"
                if token._.term == "color_term" and token.shape_ in const.TITLE_SHAPES:
                    continue

                # Skip dashes
                if token.text in const.DASH:
                    continue

                # Color is noted as missing
                if token._.term == "color_missing":
                    ent._.data["missing"] = True
                    continue

                frag = self.replace.get(token.lower_, token.lower_)

                # Skip duplicate colors within the entity
                if frag not in frags:
                    frags.append(frag)

            # Build the color
            value = "-".join(frags)
            ent._.data["color"] = self.replace.get(value, value)

        return doc
