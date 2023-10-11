import spacy

from traiter.pylib.pipes import extensions, sentence, tokenizer
from traiter.pylib.traits import color, date_, elevation, geocoordinates, habitat


def build():
    extensions.add_extensions()

    nlp = spacy.load(
        "en_core_web_sm",
        exclude=["ner", "lemmatizer", "tok2vec"],
    )

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    color.build(nlp)
    date_.build(nlp)
    elevation.build(nlp)
    habitat.build(nlp)
    geocoordinates.build(nlp)

    return nlp
