from spacy.tokens import Doc, Span


def clear_tokens(ent: Span) -> None:
    if "" not in ent.doc.vocab.strings:
        ent.doc.vocab.strings.add("")
    ent.label = ent.doc.vocab.strings[""]
    for token in ent:
        token.ent_type = ent.doc.vocab.strings[""]
        token._.flag = ""


def intern_string(doc: Doc, string: str) -> None:
    if string not in doc.vocab.strings:
        doc.vocab.strings.add(string)
