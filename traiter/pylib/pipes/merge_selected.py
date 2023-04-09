import json
from pathlib import Path

from spacy.language import Language

MERGE_SELECTED = "merge_selected"


@Language.factory(MERGE_SELECTED)
class MergeSelected:
    def __init__(self, nlp: Language, name: str, labels: list[str]):
        self.nlp = nlp
        self.name = name
        self.labels = labels

    def __call__(self, doc):
        with doc.retokenize() as retokenizer:
            for ent in [e for e in doc.ents if e.label_ in self.labels]:
                label = ent.label_
                data = ent._.data
                attrs = {
                    "ENT_TYPE": label,
                    "ENT_IOB": 3,
                    "POS": ent.root.pos_,
                    "_": {"data": data},
                }
                retokenizer.merge(ent, attrs=attrs)
        return doc

    def to_disk(self, path, exclude=tuple()):  # noqa
        path = Path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        with data_path.open("w", encoding="utf8") as data_file:
            data_file.write(json.dumps(self.labels))

    def from_disk(self, path, exclude=tuple()):  # noqa
        data_path = Path(path) / "data.json"
        with data_path.open("r", encoding="utf8") as data_file:
            self.labels = json.load(data_file)
