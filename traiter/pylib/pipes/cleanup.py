import json
from pathlib import Path
from typing import Optional

from spacy.language import Language
from spacy.tokens import Doc

CLEANUP_TRAITS = "cleanup_traits"


@Language.factory(CLEANUP_TRAITS)
class CleanupTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        keep: Optional[list[str]] = None,  # List of trait labels to keep
        clear: bool = True,
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.keep = keep if keep else []
        self.clear = clear

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete or ent.label_ not in self.keep:
                self.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.set_ents(entities)
        return doc

    def clear_tokens(self, ent):
        if self.clear:
            for token in ent:
                token._.data = {}
                token._.flag = ""
                token._.term = ""

    def to_disk(self, path, exclude=None):
        path = Path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        fields = {k: v for k, v in self.__dict__.items() if k not in ("nlp", "name")}
        with data_path.open("w", encoding="utf8") as data_file:
            data_file.write(json.dumps(fields))

    def from_disk(self, path, exclude=None):
        data_path = Path(path) / "data.json"
        with data_path.open("r", encoding="utf8") as data_file:
            data = json.load(data_file)
            for key in data:
                self.__dict__[key] = data[key]
