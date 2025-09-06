from dataclasses import asdict, dataclass
from typing import Any

from spacy.language import Language
from spacy.tokens import Span


@dataclass(eq=False)
class Base:
    _trait: str | None = None
    _text: str | None = None
    start: int | None = None
    end: int | None = None

    def __eq__(self, other: "Base") -> bool:
        return self.to_dict() == other.to_dict()

    @classmethod
    def from_ent(cls, ent: Span, **kwargs: Any) -> "Base":
        kwargs["start"] = ent.start_char
        kwargs["end"] = ent.end_char
        kwargs["_trait"] = ent.label_
        kwargs["_text"] = ent.text
        return cls(**kwargs)

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k[0] != "_"}

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        raise NotImplementedError
