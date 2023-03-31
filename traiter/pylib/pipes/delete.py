import json
from pathlib import Path

from spacy.language import Language
from spacy.tokens import Doc

DELETE_TRAITS = "traiter_delete_traits_v3"


@Language.factory(DELETE_TRAITS)
class DeleteTraits:
    def __init__(self, nlp: Language, name: str, delete: list[str] = None):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.delete = delete if delete else []  # List of traits to delete

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete:
                self.clear_tokens(ent)
                continue

            if ent.label_ in self.delete:
                self.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.set_ents(entities)
        return doc

    def to_disk(self, path, exclude=tuple()):  # noqa
        path = Path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        with data_path.open("w", encoding="utf8") as data_file:
            data_file.write(json.dumps(self.delete))

    def from_disk(self, path, exclude=tuple()):  # noqa
        data_path = Path(path) / "data.json"
        with data_path.open("r", encoding="utf8") as data_file:
            self.delete = json.load(data_file)

    @staticmethod
    def clear_tokens(ent):
        for token in ent:
            token._.data = {}
            token._.flag = ""
            token._.term = ""
