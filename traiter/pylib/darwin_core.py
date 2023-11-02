from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

DYN = "dwc:dynamicProperties"
NS = "dwc:"
SEP = " | "


@dataclass
class DarwinCore:
    props: dict[str, Any] = field(default_factory=lambda: defaultdict(list))
    dyn_props: dict[str, Any] = field(default_factory=lambda: defaultdict(list))

    def to_dict(self) -> dict:
        out = {}

        for key, values in self.props.items():
            out[key] = self.convert_value_list(key, values)

        if self.dyn_props:
            out[DYN] = {}
            for key, values in self.dyn_props.items():
                out[DYN][key] = self.convert_value_list(key, values)

        return out

    @staticmethod
    def convert_value_list(key, values):
        if all(isinstance(v, str) for v in values):
            return SEP.join(values)
        elif all(isinstance(v, tuple) for v in values):
            return SEP.join(f'"{i[0]}":"{i[1]}"' for i in values)
        elif len(values) == 1:
            return values[0]
        raise ValueError(f"Field: {key} has mixed value types")

    def add(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None:
                self.props[self.ns(key)].append(value)
        return self

    def add_dyn(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None:
                self.dyn_props[key].append(value)
        return self

    @staticmethod
    def ns(name):
        return NS + name

    def items(self):
        yield from {k: v for k, v in self.props.items() if k != DYN}.items()
        if self.props[DYN]:
            yield from self.props[DYN].items()

    @staticmethod
    def key(*args, prepend: str = None) -> str:
        key = [prepend] if prepend else []
        key += list(args)
        key = " ".join(key).replace("-", " ").split()
        key = [k.title() for k in key]
        key[0] = key[0].lower()
        key = "".join(key)
        return key
