"""Parse testes state notations."""

from pyparsing import Regex, Word, Group, Optional
from lib.base_trait import BaseTrait
from lib.parse_result import ParseResult
import lib.shared_parser_patterns as sp


class TestesState(BaseTrait):
    """Parser logic."""

    def build_parser(self):  # pylint: disable=too-many-locals
        """Return the trait parser."""
        label = (
            sp.kwd('reproductive')
            + (sp.kwd('data') | sp.kwd('state') | sp.kwd('condition'))
        )
        testes = (
            sp.kwd('testicles') | sp.kwd('testes') | sp.kwd('testis')
            | sp.kwd('test')
        )
        fully = (
            sp.kwd('fully') | sp.kwd('incompletely') | sp.kwd('completely')
            | sp.kwd('complete')
        )
        non = (
            sp.kwd('not') | sp.kwd('non') | sp.kwd('no') | sp.kwd('semi')
            | sp.kwd('sub')
        )
        descended = (
            sp.kwd('undescended') | sp.kwd('undescend') | sp.kwd('undesc')
            | sp.kwd('undes') | sp.kwd('descended') | sp.kwd('descend')
            | sp.kwd('desc') | sp.kwd('des') | sp.kwd('undecended')
            | sp.kwd('undecend') | sp.kwd('decended') | sp.kwd('decend')
            | sp.kwd('undesended') | sp.kwd('undesend') | sp.kwd('desended')
            | sp.kwd('desend')
        )
        abbrev = sp.kwd('tes') | sp.kwd('ts') | Regex(r'\b t \b', sp.flags)
        scrotal = sp.kwd('scrotum') | sp.kwd('scrotal') | sp.kwd('scrot')
        partially = sp.kwd('partially') | sp.kwd('part')
        state_abbrev = sp.kwd('scr') | sp.kwd('ns') | sp.kwd('sc')
        abdominal = sp.kwd('abdominal') | sp.kwd('abdomin') | sp.kwd('abdom')
        size = sp.kwd('visible') | sp.kwd('enlarged') | sp.kwd('small')
        gonads = (sp.kwd('gonads') | sp.kwd('gonad'))('ambiguous_sex')
        other = (
            sp.kwd('cryptorchism') | sp.kwd('cryptorchid')
            | sp.kwd('monorchism') | sp.kwd('monorchid')
            | sp.kwd('inguinal') | sp.kwd('nscr')
        )
        length = Optional(sp.cross + Optional(sp.len_units))

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

        parser.ignore(Word(sp.punct))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        parts = match[0].asDict()
        result = ParseResult()
        result.vocabulary_value(parts['value'])
        result.is_flag_in_dict(parts, 'ambiguous_sex')
        result.ends(match[1], match[2])
        return result
