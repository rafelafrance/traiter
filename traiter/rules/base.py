import sys
from dataclasses import asdict, dataclass
from typing import Any

from spacy.language import Language
from spacy.tokens import Span


@dataclass(eq=False)
class Base:
    _trait: str = ""
    _text: str = ""
    start: int = sys.maxsize
    end: int = -1

    def __eq__(self, other: "Base") -> bool:
        return self.to_dict() == other.to_dict()

    @classmethod
    def from_ent(cls, ent: Span, **kwargs: Any) -> Any:
        kwargs["start"] = kwargs.get("start", ent.start_char)
        kwargs["end"] = kwargs.get("end", ent.end_char)
        kwargs["_trait"] = kwargs.get("_trait", ent.label_)
        kwargs["_text"] = kwargs.get("_text", ent.text)
        return cls(**kwargs)

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k[0] != "_"}

    @classmethod
    def pipe(cls, nlp: Language) -> None:
        raise NotImplementedError
