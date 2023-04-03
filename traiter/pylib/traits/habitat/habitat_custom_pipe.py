from dataclasses import dataclass

from spacy import Language

from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

HABITAT_CUSTOM_PIPE = "habitat_custom_pipe"


@Language.factory(HABITAT_CUSTOM_PIPE)
@dataclass()
class HabitatPipe(BaseCustomPipe):
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == "habitat"]:
            frags = [self.replace.get(t.lower_, t.lower_) for t in ent]
            ent._.data["habitat"] = " ".join(frags)
        return doc
