"""Parse life stage notations."""

from pyparsing import Regex, Word
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class LifeStage(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = Regex(rx.boundary(
            r""" life \s* stage (?: \s* remarks )?
                 | age \s* class
                 | age \s* in \s* (?: hour | day ) s?
                 | age """), rx.flags)

        keyless = Regex(rx.boundary(
            r""" (?: after \s+ )?
                    (?: first | second | third | fourth | hatching
                        | 1st | 2nd | 3rd | \dth) \s+ year
                 | larves? |larvae? | larvals? | imagos? | neonates?
                 | hatchlings? | hatched
                 | fry
                 | metamorphs?
                 | premetamorphs?
                 | tadpoles?
                 | têtard
                 | young-of-the-year
                 | leptocephales? | leptocephalus
                 | immatures? | imms?
                 | young (?: \s* adult)? | ygs?
                 | fleglings? | fledgelings?
                 | chicks?
                 | nestlings?
                 | juveniles? | juvéniles? | juvs? | jeunes?
                 | subadults? | subadultes? | subads? | sub-adults?
                 | adults? | adulte? | ads?
                 | yearlings?
                 | matures?
                 | yolk \s* sac """), rx.flags)
        # | embryos? | embryonic | fetus (:? es )?

        word = Regex(rx.boundary(
            r' (?! determin \w+ ) \w [\w?./-]* ', right=False), rx.flags)
        sep = Regex(r' [;,"?] | $ ', rx.flags)

        word_plus = keyless | word

        parser = (
            (keyword + (word_plus + Word('/-') + keyless)('value'))
            | (keyword + (word_plus*(1, 4))('value') + sep)
            | (keyword + (word_plus + keyless)('value'))
            | (keyword + keyless('value'))
            | keyless('value')
        )

        ignore = Word(rx.punct, excludeChars='.,;"?/-')
        parser.ignore(ignore)
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        result = Result()
        result.vocabulary_value(match[0].value)
        result.ends(match[1], match[2])
        return result
