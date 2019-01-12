"""Parse testes state notations."""

from pyparsing import Regex, Word, Group, Optional, ParserElement
from lib.base_trait import BaseTrait
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp

ParserElement.enablePackrat()


class TestesState(BaseTrait):
    """Parser logic."""

    def build_parser(self):  # pylint: disable=too-many-locals
        """Return the trait parser."""
        label = (
            stp.kwd('reproductive')
            + (stp.kwd('data') | stp.kwd('state') | stp.kwd('condition'))
        )
        testes = (
            stp.kwd('testicles') | stp.kwd('testes') | stp.kwd('testis')
            | stp.kwd('test')
        )
        fully = (
            stp.kwd('fully') | stp.kwd('incompletely') | stp.kwd('completely')
            | stp.kwd('complete')
        )
        non = (
            stp.kwd('not') | stp.kwd('non') | stp.kwd('no') | stp.kwd('semi')
            | stp.kwd('sub')
        )
        descended = (
            stp.kwd('undescended') | stp.kwd('undescend') | stp.kwd('undesc')
            | stp.kwd('undes') | stp.kwd('descended') | stp.kwd('descend')
            | stp.kwd('desc') | stp.kwd('des') | stp.kwd('undecended')
            | stp.kwd('undecend') | stp.kwd('decended') | stp.kwd('decend')
            | stp.kwd('undesended') | stp.kwd('undesend') | stp.kwd('desended')
            | stp.kwd('desend')
        )
        abbrev = stp.kwd('tes') | stp.kwd('ts') | Regex(r'\b t \b', stp.flags)
        scrotal = stp.kwd('scrotum') | stp.kwd('scrotal') | stp.kwd('scrot')
        partially = stp.kwd('partially') | stp.kwd('part')
        state_abbrev = stp.kwd('scr') | stp.kwd('ns') | stp.kwd('sc')
        abdominal = (
            stp.kwd('abdominal') | stp.kwd('abdomin') | stp.kwd('abdom'))
        size = stp.kwd('visible') | stp.kwd('enlarged') | stp.kwd('small')
        gonads = (stp.kwd('gonads') | stp.kwd('gonad'))('ambiguous_sex')
        other = (
            stp.kwd('cryptorchism') | stp.kwd('cryptorchid')
            | stp.kwd('monorchism') | stp.kwd('monorchid')
            | stp.kwd('inguinal') | stp.kwd('nscr')
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
