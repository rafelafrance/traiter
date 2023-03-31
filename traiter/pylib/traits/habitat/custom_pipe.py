import json
from dataclasses import dataclass

from spacy import Language
from spacy.util import ensure_path

from traiter.pylib.traits.base_custom_pipe import BaseCustomPipe

CUSTOM_PIPE = "habitat_pipe"


@Language.component(CUSTOM_PIPE)
@dataclass()
class HabitatPipe(BaseCustomPipe):
    nlp: Language
    name: str
    trait: str
    replace: dict[str, str]

    def __call__(self, doc):
        for ent in [e for e in doc.ents if e.label_ == self.trait]:
            frags = [self.replace.get(t.lower_, t.lower_) for t in ent]
            ent._.data[self.trait] = " ".join(frags)
        return doc

    def to_disk(self, path, exclude=tuple()):  # noqa
        path = ensure_path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        with data_path.open("w", encoding="utf8") as data_file:
            data_file.write(json.dumps(self.__dict__))

    def from_disk(self, path, exclude=tuple()):  # noqa
        data_path = path / "data.json"
        with data_path.open("r", encoding="utf8") as data_file:
            data = json.load(data_file)
            for key in data.keys():
                self.__dict__[key] = data[key]
