from dataclasses import asdict, dataclass

from spacy.language import Language


@dataclass
class Base:
    trait: str = None
    start: int = None
    end: int = None

    def clean_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_ent(cls, ent, **kwargs):
        kwargs["trait"] = ent.label_
        kwargs["start"] = ent.start_char
        kwargs["end"] = ent.end_char
        return cls(**kwargs)

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError
