from dataclasses import asdict, dataclass

from spacy.language import Language


@dataclass(eq=False)
class Base:
    start: int = None
    end: int = None
    _trait: str = None
    _text: str = None

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    @classmethod
    def from_ent(cls, ent, **kwargs):
        kwargs["start"] = ent.start_char
        kwargs["end"] = ent.end_char
        kwargs["_trait"] = ent.label_
        kwargs["_text"] = ent.text
        return cls(**kwargs)

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k[0] != "_"}

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError
