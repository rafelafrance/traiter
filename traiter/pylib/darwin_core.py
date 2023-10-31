import json
import xml.etree.ElementTree as Etree
from dataclasses import dataclass, field
from typing import Any

DYN = "dwc:dynamicProperties"
NS = "dwc:"


@dataclass
class DarwinCore:
    props: dict[str, Any] = field(default_factory=lambda: {DYN: {}})

    def add(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None:
                self.props[self.ns(key)] = value
        return self

    def add_dyn(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None:
                self.props[DYN][key] = value
        return self

    @staticmethod
    def ns(name):
        return NS + name

    def items(self):
        yield from {k: v for k, v in self.props.items() if k != DYN}.items()
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

    def to_dict(self) -> dict:
        props = {k: v for k, v in self.props.items()}
        if not props[DYN]:
            del props[DYN]
        return props

    @staticmethod
    def to_xml(records: list["DarwinCore"]) -> bytes:
        doc = Etree.Element(
            "SimpleDarwinRecordSet",
            attrib={
                "xmlns": "http://rs.tdwg.org/dwc/xsd/simpledarwincore/",
                "xmlns:dc": "http://purl.org/dc/terms/",
                "xmlns:dwc": "http://rs.tdwg.org/dwc/terms/",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            },
        )

        for rec in records:
            dwc_rec = Etree.SubElement(doc, "SimpleDarwinRecord")
            for tag, text in rec.props.items():
                if tag == DYN:
                    if text:
                        text = json.dumps(text)
                    else:
                        continue
                sub = Etree.SubElement(dwc_rec, tag)
                sub.text = text

        return Etree.tostring(doc, "utf-8")
