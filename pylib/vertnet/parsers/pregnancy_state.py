"""Parse pregnancy state notations."""

from pylib.stacked_regex.rule import frag, vocab, producer
from pylib.vertnet.parsers.base import Base, convert
from pylib.vertnet.shared_reproductive_patterns import RULE


PREGNANCY_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['none'],

        vocab('pregnant', r"""
            prega?n?ant pregnan preg pregnancy pregnancies
            gravid multiparous nulliparous parous """.split()),

        vocab('joiner', r""" of were """.split()),

        vocab('recent', r"""
            recently recent was previously prev """.split()),

        vocab('probably', r"""
            probably prob possibly possible
            appears? very
            visible visibly
            evidence evident
            """.split()),

        vocab('stage', r' early late mid '.split()),

        frag('quest', '[?]'),

        frag('separator', r' [;,"] '),

        # Skip arbitrary words
        frag('word', r' [a-z]\w+ '),

        # E.g.: pregnancy visible
        producer(convert, [
            """(?P<value> pregnant joiner? none? probably quest? )"""]),

        # E.g.: Probably early pregnancy
        producer(convert, [
            """(?P<value> none? (recent | probably)?
            stage? (none | joiner)? pregnant quest? )"""]),
    ],
)
