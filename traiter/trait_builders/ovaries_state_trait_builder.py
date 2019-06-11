"""Parse testes state notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder


class OvariesStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self._build_token_rules()
        self._build_replace_rules()
        self._build_product_rules()

        self.compile_regex()

    def _build_token_rules(self):
        # self.kwd('label', r' reproductive .? (data |state | condition) ')
        self.lit('ovary', r' (ovaries | ovary s? ) \b ')

        self.kwd('size', r"""
            (enlarged | enlarge | large
                | small
                | moderate | mod
            ) ( \s+ size d? )?
            """)
        self.kwd('uterus', r' uterus | uterine ')
        self.kwd('fallopian', r' fallopian \s* ( tubes? )? ')
        self.kwd('immature', r' immature | mature ')
        self.kwd('horns', r' horns? ')
        self.kwd('covered', r' covered ')
        self.kwd('fat', r' fat ')
        self.kwd('corpus', r' corpus | corpora | corp | cor | c ')
        self.kwd('alb', r' albicans | alb ')
        self.kwd('lut', r' luteum | lute | lut ')
        self.kwd('side', r' (?P<side> both | left | right | [lr]) ')
        self.kwd('color', r""" ( dark | light | pale )? \s* (red | pink) """)

        self.lit('sign', r' \+ | \- ')
        self.lit('and', r' and | & ')
        self.lit('word', r' [a-z]+ ')

    def _build_replace_rules(self):
        self.replace('ovaries', r""" 
            ovary ( ( ( and )? uterus ( horns )? ) 
                    | ( and )? fallopian )?""")
        self.replace('coverage', r' covered (word){0,2} fat ')
        self.replace('luteum', r' ( sign )? ( corpus )? (alb | lut) ')

    def _build_product_rules(self):
        self.product(self.double, r"""
            ovaries (?P<side1> side) (?P<value1> ( word )? luteum) 
                (?P<side2> side) (?P<value2> ( word )? luteum)
            """)

        self.product(
            self.convert, r"""
            side ovaries (word){0,3} (?P<value> color)
            | ovaries (?P<value> ( size ) ( immature )? )
            | ovaries (?P<value> ( size )? ( immature ) )
            | ovaries (?P<value> coverage)
            | ovaries (?P<value> color)
            | (?P<value> luteum) ( side )? ovaries
            | ovaries ( side )? luteum
            """)

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        trait = Trait(
            value=token.groups['value'].lower(),
            start=token.start,
            end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_value_in_token('side', token)
        return trait

    @staticmethod
    def double(token):
        """Convert a single token into multiple (two) trait_builders."""
        trait1 = Trait(
            value=token.groups['value1'].lower(),
            side=token.groups['side1'].lower(),
            start=token.start,
            end=token.end)
        trait2 = Trait(
            value=token.groups['value2'].lower(),
            side=token.groups['side2'].lower(),
            start=token.start,
            end=token.end)
        return [trait1, trait2]
