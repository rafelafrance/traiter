"""Parse life stage notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder


class LifeStageTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        # JSON keys for life stage
        self.keyword('json_key', [
            r' life \s * stage \s * (remarks?)? ',
            r' age \s * class ',
            r' age \s * in \s * (?P<time_units> hours?) ',
            r' age \s * in \s * (?P<time_units> days?) ',
            r' age ',
        ])

        # Life stage is sometimes reported as an age
        self.keyword('year_num', r"""
            ( after \s* )?
            ( first | second | third | fourth | 1st | 2nd | 3rd | 4th
                | hatching ) \s*
            (?P<time_units> years? )
            """)

        # These words are life stages without a keyword indicator
        self.keyword('intrinsic', [
            r' yolk \s? sac',
            r' young [\s-]? of [\s-]? the [\s-]? year',
            r' young \s* adult',
            ]
            + """
                ads? adulte?s?
                chicks?
                fledgelings? fleglings?
                fry
                hatched hatchlings?
                imagos?
                imms? immatures?
                jeunes? juvs? juveniles? juvéniles?
                larvae? larvals? larves?
                leptocephales? leptocephalus
                matures? metamorphs?
                neonates?
                nestlings?
                nulliparous
                premetamorphs?
                sub-adults? subads? subadulte?s?
                tadpoles?
                têtard
                yearlings?
                yg ygs young
            """.split())

        # This indicates that the following words are NOT a life stage
        self.keyword('determined', r' determin \w* ')

        # Match any word
        self.fragment('word', r' \b \w [\w?./-]* (?! [./-] ) ')

        # Compound words separated by dashes or slashes
        # E.g. adult/juvenile or over-winter
        self.fragment('joiner', r' \s* [/-] \s* ')

        # Use this to find the end of a life stage pattern
        self.fragment('sep', r' [;,"?] | $ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [

            # E.g.: life stage juvenile/yearling
            'json_key (?P<value> ( intrinsic | word ) joiner intrinsic )',

            # E.g.: life stage young adult
            'json_key (?P<value> ( intrinsic | word ) intrinsic )',

            # E.g.: life stage yearling
            'json_key (?P<value> intrinsic )',

            # A sequence of words bracketed by a keyword and a separator
            # E.g.: LifeStage Remarks: 5-6 wks;
            'json_key (?P<value> ( intrinsic | word | joiner ){1,5} ) sep',

            # E.g.: LifeStage = 1st month
            'json_key (?P<value> year_num )',

            # E.g.: Juvenile
            '(?P<value> intrinsic )',

            # E.g.: 1st year
            '(?P<value> year_num )',
        ])

    @staticmethod
    def convert(token):
        """Convert parsed tokens into a result."""
        return Trait(value=token.groups['value'].lower(),
                     start=token.start, end=token.end)
