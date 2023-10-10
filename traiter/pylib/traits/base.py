class Base:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    def __str__(self):
        return str(self.as_dict())

    def __repr__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None and k[0] != "_"}

    @classmethod
    def from_ent(cls, ent, **kwargs):
        return cls(trait=ent.label_, start=ent.start_char, end=ent.end_char, **kwargs)
