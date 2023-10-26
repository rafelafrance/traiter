from traiter.pylib import pipeline
from traiter.pylib.util import compress

PIPELINE = pipeline.build()


def parse(text: str) -> list:
    text = compress(text)
    doc = PIPELINE(text)

    traits = [e._.trait for e in doc.ents]

    return traits


def to_ent(label: str, text: str):
    doc = PIPELINE(text)
    ent = next(e for e in doc.ents if e.label_ == label)
    return ent
