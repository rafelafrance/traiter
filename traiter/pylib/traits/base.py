from dataclasses import asdict, dataclass

from spacy.language import Language

from ..darwin_core import DarwinCore


@dataclass
class Base:
    trait: str = None
    start: int = None
    end: int = None

    @classmethod
    def from_ent(cls, ent, **kwargs):
        kwargs["trait"] = ent.label_
        kwargs["start"] = ent.start_char
        kwargs["end"] = ent.end_char
        return cls(**kwargs)

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError

    def clean_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}

    def to_dwc(self, dwc: DarwinCore, _ent) -> None:
        dwc.add_dyn(**self.clean_dict())
