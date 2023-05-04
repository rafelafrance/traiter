import spacy

from traiter.pylib.pipes import extensions
from traiter.pylib.pipes import sentence
from traiter.pylib.pipes import tokenizer
from traiter.pylib.traits import color
from traiter.pylib.traits import date_
from traiter.pylib.traits import elevation
from traiter.pylib.traits import habitat
from traiter.pylib.traits import lat_long


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
    lat_long.build(nlp)

    if model_path:
        nlp.to_disk(model_path)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
