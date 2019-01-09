"""Parse life stage notations."""

from pyparsing import Regex, Word, Group
from lib.base_trait import BaseTrait
from lib.parse_result import ParseResult
import lib.shared_parser_patterns as sp


class LifeStage(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = (
            Group(sp.kwd('life') + sp.kwd('stage') + sp.kwd('remarks'))
            | Group(sp.kwd('lifestage') + sp.kwd('remarks'))
            | sp.kwd('lifestageremarks')
            | Group(sp.kwd('life') + sp.kwd('stage'))
            | sp.kwd('lifestage')
            | Group(sp.kwd('age') + sp.kwd('class'))
            | sp.kwd('ageclass')
            | Group(sp.kwd('age') + sp.kwd('in') + sp.kwd('hours'))
            | sp.kwd('ageinhours')
            | Group(sp.kwd('age') + sp.kwd('in') + sp.kwd('days'))
            | sp.kwd('ageindays')
            | sp.kwd('age')
        )

        years = (
            sp.kwd('first') | sp.kwd('second')
            | sp.kwd('third') | sp.kwd('fourth')
            | sp.kwd('1st') | sp.kwd('2nd') | sp.kwd('3rd') | sp.kwd('4th')
            | sp.kwd('hatching')
         )

        keyless = (
            Group(sp.kwd('after') + years + sp.kwd('year'))
            | Group(years + sp.kwd('year'))
            | sp.kwd('larves') | sp.kwd('larvae') | sp.kwd('larva')
            | sp.kwd('larvals') | sp.kwd('larval')
            | sp.kwd('imagos') | sp.kwd('imago')
            | sp.kwd('neonates') | sp.kwd('neonates')
            | sp.kwd('hatchlings') | sp.kwd('hatchling') | sp.kwd('hatched')
            | sp.kwd('fry')
            | sp.kwd('metamorphs') | sp.kwd('metamorph')
            | sp.kwd('premetamorphs') | sp.kwd('premetamorph')
            | sp.kwd('tadpoles') | sp.kwd('tadpole')
            | sp.kwd('têtard')
            | sp.kwd('young-of-the-year')
            | sp.kwd('leptocephales') | sp.kwd('leptocephale')
            | sp.kwd('leptocephalus')
            | sp.kwd('immatures') | sp.kwd('immature')
            | sp.kwd('imms') | sp.kwd('imm')
            | sp.kwd('young adult') | sp.kwd('young')
            | sp.kwd('ygs') | sp.kwd('yg')
            | sp.kwd('fleglings') | sp.kwd('flegling')
            | sp.kwd('fledgelings') | sp.kwd('fledgeling')
            | sp.kwd('chicks') | sp.kwd('chick')
            | sp.kwd('nestlings') | sp.kwd('nestling')
            | sp.kwd('juveniles') | sp.kwd('juvenile')
            | sp.kwd('juvéniles') | sp.kwd('juvénile')
            | sp.kwd('juvs') | sp.kwd('juv')
            | sp.kwd('jeunes') | sp.kwd('jeune')
            | sp.kwd('subadults') | sp.kwd('subadult')
            | sp.kwd('subadultes') | sp.kwd('subadulte')
            | sp.kwd('subads') | sp.kwd('subad')
            | sp.kwd('sub-adults') | sp.kwd('sub-adult')
            | sp.kwd('adults') | sp.kwd('adult') | sp.kwd('adulte')
            | sp.kwd('ads') | sp.kwd('ad')
            | sp.kwd('yearlings') | sp.kwd('yearling')
            | sp.kwd('matures') | sp.kwd('mature')
            | sp.kwd('yolk sac') | sp.kwd('yolksac')
        )

        word = Regex(r' \b (?! determin \w+ ) \w [\w?./-]* ', sp.flags)

        sep = Regex(r' [;,"?] | $ ', sp.flags)

        word_plus = keyless | word

        parser = (
            (keyword + (word_plus + Word('/-') + keyless)('value'))
            | (keyword + (word_plus*(1, 4))('value') + sep)
            | (keyword + (word_plus + keyless)('value'))
            | (keyword + keyless('value'))
            | keyless('value')
        )

        parser.ignore(Word(sp.punct, excludeChars='.,;"?/-'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        print(match)
        result = ParseResult()
        result.vocabulary_value(match[0].value)
        result.ends(match[1], match[2])
        return result
