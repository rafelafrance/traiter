import spacy

from traiter.pylib.pipes import extensions
from traiter.pylib.pipes import sentence
from traiter.pylib.pipes import tokenizer
from traiter.pylib.traits.color import color_pipeline
from traiter.pylib.traits.date import date_pipeline
from traiter.pylib.traits.elevation import elevation_pipeline
from traiter.pylib.traits.habitat import habitat_pipeline
from traiter.pylib.traits.lat_long import lat_long_pipeline


# from .pipes import debug  # #########################
# debug.tokens(nlp)  # ################################


def build(model_path=None):
    extensions.add_extensions()

    nlp = spacy.load(
        "en_core_web_sm",
        exclude=["ner", "lemmatizer", "tok2vec"],
    )

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    color_pipeline.build(nlp)
    date_pipeline.build(nlp)
    elevation_pipeline.build(nlp)
    habitat_pipeline.build(nlp)
    lat_long_pipeline.build(nlp)

    if model_path:
        nlp.to_disk(model_path)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
