from spacy import Language

FINSH = "finish_terms"


@Language.component(FINSH)
def finish_terms(doc):
    for ent in doc.ents:
        ent._.data["trait"] = ent._.data.get("trait", ent.label_)
        ent._.data["start"] = ent._.data.get("start", ent.start_char)
        ent._.data["end"] = ent._.data.get("end", ent.end_char)
    return doc
