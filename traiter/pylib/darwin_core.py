import json
import xml.etree.ElementTree as Etree
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DarwinCore:
    recs: list[dict[str, Any]] = field(default_factory=list)

    def new_rec(self):
        self.recs.append({"dynamicProperties": {}})

    def add(self, idx=-1, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                self.recs[idx][key] = value

    def add_dyn(self, idx=-1, **kwargs) -> None:
        for key, value in kwargs.items():
            if value is not None:
                self.recs[idx]["dynamicProperties"][key] = value

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
        """Convert a single record to a dict for testing."""
        props = deepcopy(self.recs[idx])
        if not props["dynamicProperties"]:
            del props["dynamicProperties"]
        return props

    def to_json(self):
        recs = [self.to_dict(i) for i in range(len(self.recs))]
        return json.dumps(recs)

    def to_jsonl(self):
        recs = [self.to_dict(i) for i in range(len(self.recs))]
        return [json.dumps(r) + "\n" for r in recs]

    def to_xml(self) -> bytes:
        ns = {
            "xmlns": "http://rs.tdwg.org/dwc/xsd/simpledarwincore/",
            "xmlns:dc": "http://purl.org/dc/terms/",
            "xmlns:dwc": "http://rs.tdwg.org/dwc/terms/",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
        doc = Etree.Element("SimpleDarwinRecordSet", attrib=ns)

        for rec in self.recs:
            dwc_rec = Etree.SubElement(doc, "SimpleDarwinRecord")
            for tag, text in rec.items():
                if tag == "dynamicProperties" and text:
                    text = json.dumps(text)
                sub = Etree.SubElement(dwc_rec, "dwc:" + tag)
                sub.text = text

        return Etree.tostring(doc, "utf-8")
