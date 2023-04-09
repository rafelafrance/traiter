import spacy

from . import tokenizer
from .pipes import extensions
from .pipes.sentence import SENTENCES
from .traits.color import color_pipeline
from .traits.date import date_pipeline
from .traits.elevation import elevation_pipeline
from .traits.habitat import habitat_pipeline
from .traits.lat_long import lat_long_pipeline

# from .pipes import debug  # #########################
# debug.tokens(nlp)  # ################################


def build(model_path=None):
    extensions.add_extensions()

    nlp = spacy.load(
        "en_core_web_sm",
        exclude=["ner", "parser", "lemmatizer", "tok2vec", "attribute_ruler"],
    )

    tokenizer.setup_tokenizer(nlp)

    color_pipeline.build(nlp)
    date_pipeline.build(nlp)
    elevation_pipeline.build(nlp)
    habitat_pipeline.build(nlp)
    lat_long_pipeline.build(nlp)

    nlp.add_pipe(SENTENCES)

    if model_path:
        nlp.to_disk(model_path)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
