from spacy.language import Language


class Base:
    def __init__(self, trait: str = None, start: int = None, end: int = None):
        self.trait = trait
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.as_dict())

    def __repr__(self):
        return str(self.as_dict())

    def __eq__(self, other):
        other = other if isinstance(other, dict) else other.as_dict()
        return self.as_dict() == other

    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_ent(cls, ent, **kwargs):
        kwargs["trait"] = ent.label_
        kwargs["start"] = ent.start_char
        kwargs["end"] = ent.end_char
        return cls(**kwargs)

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError
