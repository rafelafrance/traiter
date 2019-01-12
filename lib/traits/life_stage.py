"""Parse life stage notations."""

from pyparsing import Regex, Word, Group, ParserElement
from lib.base_trait import BaseTrait
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp

ParserElement.enablePackrat()


class LifeStage(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = (
            Group(stp.kwd('life') + stp.kwd('stage') + stp.kwd('remarks'))
            | Group(stp.kwd('lifestage') + stp.kwd('remarks'))
            | stp.kwd('lifestageremarks')
            | Group(stp.kwd('life') + stp.kwd('stage'))
            | stp.kwd('lifestage')
            | Group(stp.kwd('age') + stp.kwd('class'))
            | stp.kwd('ageclass')
            | Group(stp.kwd('age') + stp.kwd('in') + stp.kwd('hours'))
            | stp.kwd('ageinhours')
            | Group(stp.kwd('age') + stp.kwd('in') + stp.kwd('days'))
            | stp.kwd('ageindays')
            | stp.kwd('age')
        )

        years = (
            stp.kwd('first') | stp.kwd('second')
            | stp.kwd('third') | stp.kwd('fourth')
            | stp.kwd('1st') | stp.kwd('2nd') | stp.kwd('3rd') | stp.kwd('4th')
            | stp.kwd('hatching')
         )

        keyless = (
            Group(stp.kwd('after') + years + stp.kwd('year'))
            | Group(years + stp.kwd('year'))
            | stp.kwd('larves') | stp.kwd('larvae') | stp.kwd('larva')
            | stp.kwd('larvals') | stp.kwd('larval')
            | stp.kwd('imagos') | stp.kwd('imago')
            | stp.kwd('neonates') | stp.kwd('neonates')
            | stp.kwd('hatchlings') | stp.kwd('hatchling') | stp.kwd('hatched')
            | stp.kwd('fry')
            | stp.kwd('metamorphs') | stp.kwd('metamorph')
            | stp.kwd('premetamorphs') | stp.kwd('premetamorph')
            | stp.kwd('tadpoles') | stp.kwd('tadpole')
            | stp.kwd('têtard')
            | stp.kwd('young-of-the-year')
            | stp.kwd('leptocephales') | stp.kwd('leptocephale')
            | stp.kwd('leptocephalus')
            | stp.kwd('immatures') | stp.kwd('immature')
            | stp.kwd('imms') | stp.kwd('imm')
            | stp.kwd('young adult') | stp.kwd('young')
            | stp.kwd('ygs') | stp.kwd('yg')
            | stp.kwd('fleglings') | stp.kwd('flegling')
            | stp.kwd('fledgelings') | stp.kwd('fledgeling')
            | stp.kwd('chicks') | stp.kwd('chick')
            | stp.kwd('nestlings') | stp.kwd('nestling')
            | stp.kwd('juveniles') | stp.kwd('juvenile')
            | stp.kwd('juvéniles') | stp.kwd('juvénile')
            | stp.kwd('juvs') | stp.kwd('juv')
            | stp.kwd('jeunes') | stp.kwd('jeune')
            | stp.kwd('subadults') | stp.kwd('subadult')
            | stp.kwd('subadultes') | stp.kwd('subadulte')
            | stp.kwd('subads') | stp.kwd('subad')
            | stp.kwd('sub-adults') | stp.kwd('sub-adult')
            | stp.kwd('adults') | stp.kwd('adult') | stp.kwd('adulte')
            | stp.kwd('ads') | stp.kwd('ad')
            | stp.kwd('yearlings') | stp.kwd('yearling')
            | stp.kwd('matures') | stp.kwd('mature')
            | stp.kwd('yolk sac') | stp.kwd('yolksac')
        )

        word = Regex(r' \b (?! determin \w+ ) \w [\w?./-]* ', stp.flags)

        sep = Regex(r' [;,"?] | $ ', stp.flags)

        word_plus = keyless | word

        parser = (
            (keyword + (word_plus + Word('/-') + keyless)('value'))
            | (keyword + (word_plus*(1, 4))('value') + sep)
            | (keyword + (word_plus + keyless)('value'))
            | (keyword + keyless('value'))
            | keyless('value')
        )

        parser.ignore(Word(stp.punct, excludeChars='.,;"?/-'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        result = ParsedTrait()
        result.vocabulary_value(match[0].value)
        result.ends(match[1], match[2])
        return result
