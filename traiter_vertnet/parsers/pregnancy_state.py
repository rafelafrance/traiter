"""Parse pregnancy state notations."""

from traiter.vocabulary import Vocabulary
from traiter_vertnet.parsers.base import Base, convert
import traiter_vertnet.shared_reproductive_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

PREGNANCY_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB.term('pregnant', r"""
            prega?n?ant pregnan preg pregnancy pregnancies
            gravid multiparous nulliparous parous """.split()),

        VOCAB.term('joiner', r""" of were """.split()),

        VOCAB.term('recent', r"""
            recently recent was previously prev """.split()),

        VOCAB.term('probably', r"""
            probably prob possibly possible
            appears? very
            visible visibly
            evidence evident
            """.split()),

        VOCAB.term('stage', r' early late mid '.split()),

        VOCAB.part('separator', r' [;,"] '),

        # E.g.: pregnancy visible
        VOCAB.producer(convert, [
            """(?P<value> pregnant joiner? none? probably quest? )"""]),

        # E.g.: Probably early pregnancy
        VOCAB.producer(convert, [
            """(?P<value> none? (recent | probably)?
            stage? (none | joiner)? pregnant quest? )"""]),
    ],
)
