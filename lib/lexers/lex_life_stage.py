"""Lex life stage annotations."""

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_regexp as regexp


class LexLifeStage(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> regexp.Regexps:
        """Define the lexer."""
        return [
            regexp.Regexp('skip', r' determin \w*'),

            regexp.Regexp('key', regexp.boundary(
                r""" life \s* stage (?: \s* remarks )?
                     | age \s* class
                     | age \s* in \s* (?: hour | day ) s?
                     | age """)),

            regexp.Regexp('keyless', regexp.boundary(
                r""" (?: after \s+ )?
                        (?: first | second | third | fourth | hatching
                            | 1st | 2nd | 3rd | \dth) \s+ year
                     | larves? |larvae? | larvals? | imagos? | neonates?
                     | hatchlings? | hatched | fry | metamorphs?
                     | premetamorphs?
                     | tadpoles? | têtard
                     | young-of-the-year | leptocephales? | leptocephalus
                     | immatures? | imms? | jeunes?
                     | young (?: \s* adult)? | ygs?
                     | fleglings? | fledgelings? | chicks? | nestlings?
                     | juveniles? | juvéniles? | juvs?
                     | subadults? | subadultes? | subads? | sub-adults?
                     | yearlings? | matures? | adults? | adulte? | ads?
                     | yolk \s* sac """)),
            # | embryos? | embryonic | fetus (:? es )?

            regexp.Regexp('word_plus', regexp.boundary(r' \w [\w?./\-]* ')),

            regexp.Regexp('sep', r' [;,"?] | $ '),

            regexp.Regexp('joiner', r' [/-] '),
        ]
