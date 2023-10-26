from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DarwinCore:
    props: list[dict[str, Any]] = field(default_factory=list)

    def new_rec(self):
        self.props.append({"dynamicProperties": {}})

    def add(self, idx=-1, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                self.props[idx][key] = value

    def add_dyn(self, idx=-1, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                self.props[idx]["dynamicProperties"][key] = value

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

    def to_dict(self, idx=0) -> dict:
        props = deepcopy(self.props[idx])
        if not props["dynamicProperties"]:
            del props["dynamicProperties"]
        return props
