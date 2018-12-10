"""Lex life stage annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.base_lexer import BaseLexer, isolate


class LifeStageLexer(BaseLexer):
    """Lex testes state annotations."""

    tokens = [
        ('skip', r' determin \w*'),

        ('key', isolate(
            r""" life \s* stage (?: \s* remarks )?
                 | age \s* class
                 | age \s* in \s* (?: hour | day ) s?
                 | age """)),

        ('keyless', isolate(
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
                 | yearlings? | matures? | adults? | adulte? | ads? """)),

        ('before_birth', isolate(r' yolk \s* sac ')),
        # | embryos? | embryonic | fetus (:? es )?

        ('word_plus', isolate(r' \w [\w?./\-]* ')),

        ('stop', r' [;,"?] | $ '),

        ('joiner', r' [/-] ')]
