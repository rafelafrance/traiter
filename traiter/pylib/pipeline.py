import spacy

from traiter.pylib.pipes import extensions, sentence, tokenizer
from traiter.pylib.traits import color, date_, elevation, geocoordinates, habitat


def build(model_path=None):
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

    if model_path:
        nlp.to_disk(model_path)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
