from dataclasses import dataclass

from spacy import Language

from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE = "habitat_custom_pipe"


@Language.factory(CUSTOM_PIPE)
@dataclass()
class HabitatPipe(BaseCustomPipe):
    trait: str
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            frags = [self.replace.get(t.lower_, t.lower_) for t in ent]
            ent._.data[self.trait] = " ".join(frags)
        return doc
