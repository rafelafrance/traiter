"""Parse life stage notations."""

from lib.trait import Trait
from lib.traits.base_trait import BaseTrait


class LifeStageTrait(BaseTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('keyword', r"""
            life \s* stage \s* (?: remarks? )?
            | age \s* class
            | age \s* in \s* (?P<time_units> hours? )
            | age \s* in \s* (?P<time_units> days? )
            | age
            """)

        self.kwd('year_num', r"""
            (?: after \s* )?
            (?: first | second | third | fourth | 1st | 2nd | 3rd | 4th
            | hatching ) \s* (?P<time_units> years? )
            """)

        self.kwd('keyless', r"""
            larves? | larvae? | larvals?
            | imagos?
            | neonates?
            | hatchlings? | hatched
            | fry
            | metamorphs? | premetamorphs?
            | tadpoles? | têtard
            | young [\s-]? of [\s-]? the [\s-]? year
            | leptocephales? | leptocephalus
            | immatures? | imms?
            | young \s* adult | young | ygs | yg
            | fleglings? | fledgelings?
            | chicks?
            | nestlings?
            | juveniles? | juvéniles? | juvs? | jeunes?
            | subadulte?s? | subads? | sub-adults?
            | adulte?s? | ads?
            | yearlings?
            | matures?
            | yolk \s? sac
            """)

        self.kwd('determined', r'determin \w+')

        self.lit('word', r' \b \w [\w?./-]* (?! [./-] ) ')
        self.lit('joiner', r' \s* [/-] \s* ')
        self.lit('sep', r' [;,"?] | $ ')

        # Build rules for parsing the trait
        self.product(self.convert, r"""
            keyword (?P<value> (?: keyless | word ) joiner keyless )
            | keyword (?P<value> (?: keyless | word ) keyless )
            | keyword (?P<value> keyless )
            | keyword (?P<value> (?: keyless | word ){1,4} ) sep
            | keyword (?P<value> year_num )
            | (?P<value> keyless )
            | (?P<value> year_num )
            """)

        self.finish_init()

    def convert(self, token):  # pylint: disable=no-self-use
        """Convert parsed tokens into a result."""
        return Trait(value=token.groups['value'].lower(),
                     start=token.start, end=token.end)
