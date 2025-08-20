import spacy

from traiter.pipes import extensions, sentence, tokenizer
from traiter.rules.color import Color
from traiter.rules.date_ import Date
from traiter.rules.elevation import Elevation
from traiter.rules.habitat import Habitat
from traiter.rules.lat_long import LatLong
from traiter.rules.trs import TRS
from traiter.rules.utm import UTM
from traiter.rules.uuid import Uuid


def build() -> spacy.Language:
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    Color.pipe(nlp)
    Uuid.pipe(nlp)
    Date.pipe(nlp)
    Elevation.pipe(nlp)
    LatLong.pipe(nlp)
    Habitat.pipe(nlp)
    TRS.pipe(nlp)
    UTM.pipe(nlp)

    return nlp
