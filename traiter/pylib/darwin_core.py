import json
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
        flat = []
        for value in values:
            if isinstance(value, list):
                flat += value
            else:
                flat.append(value)
        values = flat

        if all(isinstance(v, str) for v in values):
            return SEP.join(values)

        if all(isinstance(f, float) for f in values):
            return values if len(values) > 1 else values[0]

        if all(isinstance(f, int) for f in values):
            return values if len(values) > 1 else values[0]

        if all(isinstance(v, dict) for v in values):
            new_list = []
            for val in values:
                new = ", ".join(f"{k}: {v}" for k, v in val.items())
                new_list.append(new)
            return SEP.join(json.dumps(v) for v in new_list)

        raise ValueError(f"Field: {key} has mixed value types: {values=}")

    def add(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            key = self.ns(key)
            if value is not None and value not in self.props[key]:
                self.props[key].append(value)
        return self

    def add_dyn(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None and value not in self.dyn_props[key]:
                self.dyn_props[key].append(value)
        return self

    @staticmethod
    def format_dict(value: dict) -> dict:
        """Format a dict value by removing None values and quoting strings."""
        return {k: v for k, v in value.items() if v is not None}

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
