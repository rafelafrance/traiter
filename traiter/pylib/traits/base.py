from dataclasses import asdict, dataclass


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

    def as_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
