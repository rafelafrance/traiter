def clear_tokens(ent):
    if "" not in ent.doc.vocab.strings:
        ent.doc.vocab.strings.add("")
    ent.label = ent.doc.vocab.strings[""]
    for token in ent:
        token.ent_type = ent.doc.vocab.strings[""]
        token._.flag = ""


def intern_string(doc, string):
    if string not in doc.vocab.strings:
        doc.vocab.strings.add(string)
