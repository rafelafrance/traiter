from spacy import Language


TERM_UPDATE = "term_update"


@Language.component(TERM_UPDATE)
def term_update(doc):
    for token in doc:
        if not token._.term:
            token._.term = token.ent_type_
    return doc
