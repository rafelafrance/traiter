"""Parse testes state notations."""

from traiter.parse import Parse
from traiter.traits.base_trait import BaseTrait


class OvariesStateTrait(BaseTrait):
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
        self.lit('ovary', r' (ovaries | ovary | ovas | ova) \b ')

        self.kwd('size', r"""
            (enlarged | enlarge | large
                | small
                | moderate | mod
            ) (\s+ size d?)?
            """)
        self.kwd('uterus', r' uterus | uterine ')
        self.kwd('immature', r' immature | mature ')
        self.kwd('horns', r' horns? ')
        self.kwd('covered', r' covered ')
        self.kwd('fat', r' fat ')
        self.kwd('corpus', r' corpus | corpora | corp | cor | c ')
        self.kwd('alb', r' albicans | alb ')
        self.kwd('lut', r' luteum | lute | lut ')
        self.kwd('side', r' (?P<side> both | left | right | [lr]) ')

        self.lit('sign', r' \+ | \- ')
        self.lit('and', r' and | & ')
        self.lit('word', r' [a-z]+ ')

    def _build_replace_rules(self):
        self.replace(
            'ovaries', r' ovary ( (and)? uterus (horns)? )? ')
        self.replace('coverage', r' covered (word){0,2} fat ')
        self.replace('luteum', r' (sign)? (corpus)? (alb | lut) ')

    def _build_product_rules(self):
        self.product(self.double, r"""
            ovaries (?P<side1> side) (?P<value1> (word)? luteum) 
                (?P<side2> side) (?P<value2> (word)? luteum)
            """)

        self.product(
            self.convert, r"""
            ovaries (?P<value> size)
            | ovaries (?P<value> coverage)
            | (?P<value> luteum (side)?) ovaries
            | ovaries side luteum
            """)

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        trait = Parse(
            value=token.groups['value'].lower(),
            start=token.start,
            end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
        return trait

    @staticmethod
    def double(token):
        """Convert a single token into multiple (two) traits."""
        trait1 = Parse(
            value=token.groups['value1'].lower(),
            side=token.groups['side1'].lower(),
            start=token.start,
            end=token.end)
        trait2 = Parse(
            value=token.groups['value2'].lower(),
            side=token.groups['side2'].lower(),
            start=token.start,
            end=token.end)
        return [trait1, trait2]
