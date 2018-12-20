"""Lex total length annotations."""

# pylint: disable=missing-docstring,invalid-name


from lib.lexers.lex_base import LexBase
import lib.lexers.shared_lex_rules as rule
import lib.lexers.shared_utils as util


class LexBodyMass(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> rule.LexRules:
        return [
            rule.shorthand_mass,
            rule.fraction,
            rule.range,
            rule.feet,
            rule.inches,
            rule.shorthand_key,

            rule.LexRule('key_with_units', util.boundary(
                r""" weightingrams | massingrams """)),

        ]
