"""Lex life stage annotations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_base import LexBase
import lib.lexers.shared_lex_rules as rule
import lib.lexers.shared_utils as util


class LexLifeStage(LexBase):
    """Lex testes state annotations."""

    def rule_list(self) -> rule.LexRules:
        return [
            rule.LexRule('skip', r' determin \w*'),

            rule.LexRule('key', util.boundary(
                r""" life \s* stage (?: \s* remarks )?
                     | age \s* class
                     | age \s* in \s* (?: hour | day ) s?
                     | age """)),

            rule.LexRule('keyless', util.boundary(
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

            rule.LexRule('word_plus', util.boundary(r' \w [\w?./\-]* ')),

            rule.LexRule('stop', r' [;,"?] | $ '),

            rule.LexRule('joiner', r' [/-] '),
        ]
