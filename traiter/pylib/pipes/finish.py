from spacy import Language

FINSH = "finish_terms"


@Language.component(FINSH)
def finish_terms(doc):
    for ent in doc.ents:
        ent._.data["trait"] = ent.label_
        ent._.data["start"] = ent.start_char
        ent._.data["end"] = ent.end_char
    return doc
