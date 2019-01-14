"""Parse testes state notations."""

from pyparsing import Regex, Word, Group, Optional
from pyparsing import CaselessKeyword as kwd
from lib.base_trait import BaseTrait
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp


class TestesState(BaseTrait):
    """Parser logic."""

    def build_parser(self):  # pylint: disable=too-many-locals
        """Return the trait parser."""
        label = (
            kwd('reproductive')
            + (kwd('data') | kwd('state') | kwd('condition'))
        )
        testes = (
            kwd('testicles') | kwd('testes') | kwd('testis')
            | kwd('test')
        )
        fully = (
            kwd('fully') | kwd('incompletely') | kwd('completely')
            | kwd('complete')
        )
        non = (
            kwd('not') | kwd('non') | kwd('no') | kwd('semi')
            | kwd('sub')
        )
        descended = (
            kwd('undescended') | kwd('undescend') | kwd('undesc')
            | kwd('undes') | kwd('descended') | kwd('descend')
            | kwd('desc') | kwd('des') | kwd('undecended')
            | kwd('undecend') | kwd('decended') | kwd('decend')
            | kwd('undesended') | kwd('undesend') | kwd('desended')
            | kwd('desend')
        )
        abbrev = kwd('tes') | kwd('ts') | Regex(r'\b t \b', stp.flags)
        scrotal = kwd('scrotum') | kwd('scrotal') | kwd('scrot')
        partially = kwd('partially') | kwd('part')
        state_abbrev = kwd('scr') | kwd('ns') | kwd('sc')
        abdominal = (
            kwd('abdominal') | kwd('abdomin') | kwd('abdom'))
        size = kwd('visible') | kwd('enlarged') | kwd('small')
        gonads = (kwd('gonads') | kwd('gonad'))('ambiguous_sex')
        other = (
            kwd('cryptorchism') | kwd('cryptorchid')
            | kwd('monorchism') | kwd('monorchid')
            | kwd('inguinal') | kwd('nscr')
        )

        length = Optional(stp.cross + Optional(stp.len_units))

        state = (
            Group(non + fully + descended)
            | Group(abdominal + non + descended)
            | Group(abdominal + descended)
            | Group(non + descended)
            | Group(fully + descended)
            | Group(partially + descended)
            | Group(size + non + descended)
            | Group(size + descended)
            | descended
            | size
        )

        parser = (
            (label + (testes | abbrev) + length + state('value'))
            | (label + (testes | abbrev) + length + state_abbrev('value'))
            | (label + (testes | abbrev) + length + abdominal('value'))
            | (label + (testes | abbrev) + length + scrotal('value'))
            | (label + (testes | abbrev) + length + (non + scrotal)('value'))
            | (label + (testes | abbrev) + length + other('value'))
            | (label + (testes | abbrev) + length + (non + testes)('value'))
            | (label + length + (non + testes)('value'))
            | (label + length + (non + scrotal)('value'))
            | (label + length + scrotal('value'))
            | abbrev + length + state('value')
            | abbrev + length + abdominal('value')
            | abbrev + length + (non + scrotal)('value')
            | abbrev + length + scrotal('value')
            | abbrev + length + other('value')
            | testes + length + state('value')
            | testes + length + state_abbrev('value')
            | testes + length + abdominal('value')
            | testes + length + scrotal('value')
            | testes + length + (non + scrotal)('value')
            | testes + length + other('value')
            | (non + testes)('value')
            | (non + scrotal)('value')
            | (non + gonads)('value')
            | scrotal('value')
        )

        parser.ignore(Word(stp.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        result = ParsedTrait()
        result.vocabulary_value(parts['value'])
        result.is_flag_in_dict(parts, 'ambiguous_sex')
        result.ends(match[1], match[2])
        return result
