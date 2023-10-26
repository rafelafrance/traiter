from copy import copy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DarwinCore:
    props: dict[str, Any] = field(default_factory=dict)
    dyn_props: dict[str, Any] = field(default_factory=dict)

    def add(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                self.props[key] = value

    def add_dyn(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                self.dyn_props[key] = value

    # Examples: femaleFlowerPistolShape or stemSizeInCentimeters
    @staticmethod
    def key(*args, prepend: str = None) -> str:
        key = [prepend] if prepend else []
        key += list(args)
        key = " ".join(key).replace("-", " ").split()
        key = [k.title() for k in key]
        key[0] = key[0].lower()
        key = "".join(key)
        return key

    def to_dict(self) -> dict:
        props = copy(self.props)
        if self.dyn_props:
            props["dynamicProperties"] = copy(self.dyn_props)
        return props
