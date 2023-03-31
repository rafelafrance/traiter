from dataclasses import dataclass

from spacy import Language

from ..base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE = "color_custom_pipe"


@Language.factory(CUSTOM_PIPE)
@dataclass()
class ColorPipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]
    remove: dict[str, int]
    title_shapes: list[str]
    dash_char: list[str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            frags = []

            for token in ent:
                # Skip anything that is not a term
                if not token._.term:
                    continue

                # Skip terms marked for removal
                if self.remove.get(token.lower_):
                    continue

                # Skip names like "Brown"
                if token._.term == "color_term" and token.shape_ in self.title_shapes:
                    continue

                # Skip dashes
                if token.text in self.dash_char:
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
            ent._.data[self.trait] = self.replace.get(value, value)

        return doc
