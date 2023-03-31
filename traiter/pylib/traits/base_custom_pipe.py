import json
from dataclasses import dataclass
from pathlib import Path

from spacy import Language


@dataclass()
class BaseCustomPipe:
    nlp: Language
    name: str

    def __call__(self, doc):
        raise NotImplementedError()

    def to_disk(self, path, exclude=tuple()):  # noqa
        path = Path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        fields = {k: v for k, v in self.__dict__.items() if k not in ("nlp", "name")}
        with data_path.open("w", encoding="utf8") as data_file:
            data_file.write(json.dumps(fields))

    def from_disk(self, path, exclude=tuple()):  # noqa
        data_path = Path(path) / "data.json"
        with data_path.open("r", encoding="utf8") as data_file:
            data = json.load(data_file)
            for key in data.keys():
                self.__dict__[key] = data[key]
