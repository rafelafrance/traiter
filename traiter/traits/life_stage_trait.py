"""Parse life stage notations."""

from traiter.parse import Parse
from traiter.traits.base_trait import BaseTrait


class LifeStageTrait(BaseTrait):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self._build_token_rules()
        self._build_product_rules()

        self.compile_regex()

    def _build_token_rules(self):
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

    def _build_product_rules(self):
        self.product(self.convert, r"""
            keyword (?P<value> (?: keyless | word ) joiner keyless )
            | keyword (?P<value> (?: keyless | word ) keyless )
            | keyword (?P<value> keyless )
            | keyword (?P<value> (?: keyless | word | joiner ){1,5} ) sep
            | keyword (?P<value> year_num )
            | (?P<value> keyless )
            | (?P<value> year_num )
            """)

    @staticmethod
    def convert(token):
        """Convert parsed tokens into a result."""
        return Parse(value=token.groups['value'].lower(),
                     start=token.start, end=token.end)
