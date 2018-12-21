"""Lex total length annotations."""

# pylint: disable=missing-docstring,invalid-name


from lib.lexers.lex_base import LexBase
import lib.lexers.shared_regexp as regexp


class LexBodyMass(LexBase):
    """Lex total length annotations."""

    def rule_list(self) -> regexp.Regexps:
        return [
            regexp.shorthand_mass,
            regexp.fraction,
            regexp.range,
            regexp.pounds,
            regexp.ounces,
            regexp.shorthand_key,

            regexp.Regexp('key_with_units', regexp.boundary(
                r""" weightingrams | massingrams """)),

            regexp.Regexp('wt_key', regexp.boundary(r"""
                (?: (?: body | full | observed | total ) \.? \s* )?
                    (?: weights?
                    | weigh (?: s | ed | ing )
                    | mass
                    | w \.? t s? \.? )
                | body
                """)),

            regexp.metric_mass,
        ]
