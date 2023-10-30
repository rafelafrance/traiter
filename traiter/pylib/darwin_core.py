# import json
# import xml.etree.ElementTree as Etree
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DarwinCore:
    fields: dict[str, Any] = field(default_factory=lambda: {"dynamicProperties": {}})

    def add(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None:
                self.fields[key] = value
        return self

    def add_dyn(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None:
                self.fields["dynamicProperties"][key] = value
        return self

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
        """Convert a single record to a dict for testing."""
        props = deepcopy(self.fields)
        if not props["dynamicProperties"]:
            del props["dynamicProperties"]
        return props

    # def to_json(self):
    #     fields = [self.to_dict(i) for i in range(len(self.fields))]
    #     return json.dumps(fields)
    #
    # def to_jsonl(self):
    #     fields = [self.to_dict(i) for i in range(len(self.fields))]
    #     return [json.dumps(r) + "\n" for r in fields]
    #
    # def to_xml(self) -> bytes:
    #     ns = {
    #         "xmlns": "http://rs.tdwg.org/dwc/xsd/simpledarwincore/",
    #         "xmlns:dc": "http://purl.org/dc/terms/",
    #         "xmlns:dwc": "http://rs.tdwg.org/dwc/terms/",
    #         "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    #     }
    #     doc = Etree.Element("SimpleDarwinRecordSet", attrib=ns)
    #
    #     for rec in self.fields:
    #         dwc_rec = Etree.SubElement(doc, "SimpleDarwinRecord")
    #         for tag, text in rec.items():
    #             if tag == "dynamicProperties":
    #                 if text:
    #                     text = json.dumps(text)
    #                 else:
    #                     continue
    #             sub = Etree.SubElement(dwc_rec, "dwc:" + tag)
    #             sub.text = text
    #
    #     return Etree.tostring(doc, "utf-8")
