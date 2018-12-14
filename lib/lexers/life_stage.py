"""Lex life stage annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.base import Base
from lib.lexers.util import boundary


class LexLifeStage(Base):
    """Lex testes state annotations."""

    tokens = [
        ('skip', r' determin \w*'),

        ('key', boundary(
            r""" life \s* stage (?: \s* remarks )?
                 | age \s* class
                 | age \s* in \s* (?: hour | day ) s?
                 | age """)),

        ('keyless', boundary(
            r""" (?: after \s+ )?
                    (?: first | second | third | fourth | hatching
                        | 1st | 2nd | 3rd | \dth) \s+ year
                 | larves? |larvae? | larvals? | imagos? | neonates?
                 | hatchlings? | hatched | fry | metamorphs? | premetamorphs?
                 | tadpoles? | têtard
                 | young-of-the-year | leptocephales? | leptocephalus
                 | immatures? | imms? | jeunes? | young (?: \s* adult)? | ygs?
                 | fleglings? | fledgelings? | chicks? | nestlings?
                 | juveniles? | juvéniles? | juvs?
                 | subadults? | subadultes? | subads? | sub-adults?
                 | yearlings? | matures? | adults? | adulte? | ads?
                 | yolk \s* sac """)),
        # | embryos? | embryonic | fetus (:? es )?

        ('word_plus', boundary(r' \w [\w?./\-]* ')),

        ('stop', r' [;,"?] | $ '),

        ('joiner', r' [/-] ')]
