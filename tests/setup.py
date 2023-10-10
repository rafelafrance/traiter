from traiter.pylib import pipeline
from traiter.pylib.util import compress

PIPELINE = pipeline.build()


def test(text: str) -> list[dict]:
    text = compress(text)
    doc = PIPELINE(text)

    traits = [e._.trait for e in doc.ents]

    return traits
