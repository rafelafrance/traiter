from spacy import Language


TERM_UPDATE = "term_update"


@Language.factory(TERM_UPDATE)
class TermUpdate:
    def __init__(self, nlp, name, overwrite: bool = False):
        self.nlp = nlp
        self.name = name
        self.overwrite = overwrite

    def __call__(self, doc):
        for token in doc:
            if not token._.term or self.overwrite:
                token._.term = token.ent_type_
        return doc
