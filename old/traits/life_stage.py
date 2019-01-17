"""Parse life stage notations."""

from pyparsing import Regex, Word, Group
from pyparsing import CaselessKeyword as kwd
from lib.base_trait import BaseTrait
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp


class LifeStage(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = (
            Group(kwd('life') + kwd('stage') + kwd('remarks'))
            | Group(kwd('lifestage') + kwd('remarks'))
            | kwd('lifestageremarks')
            | Group(kwd('life') + kwd('stage'))
            | kwd('lifestage')
            | Group(kwd('age') + kwd('class'))
            | kwd('ageclass')
            | Group(kwd('age') + kwd('in') + kwd('hours'))
            | kwd('ageinhours')
            | Group(kwd('age') + kwd('in') + kwd('days'))
            | kwd('ageindays')
            | kwd('age')
        )

        years = (
            kwd('first') | kwd('second')
            | kwd('third') | kwd('fourth')
            | kwd('1st') | kwd('2nd') | kwd('3rd') | kwd('4th')
            | kwd('hatching')
        )

        keyless = (
            Group(kwd('after') + years + kwd('year'))
            | Group(years + kwd('year'))
            | kwd('larves') | kwd('larvae') | kwd('larva')
            | kwd('larvals') | kwd('larval')
            | kwd('imagos') | kwd('imago')
            | kwd('neonates') | kwd('neonates')
            | kwd('hatchlings') | kwd('hatchling') | kwd('hatched')
            | kwd('fry')
            | kwd('metamorphs') | kwd('metamorph')
            | kwd('premetamorphs') | kwd('premetamorph')
            | kwd('tadpoles') | kwd('tadpole')
            | kwd('têtard')
            | kwd('young-of-the-year')
            | kwd('leptocephales') | kwd('leptocephale')
            | kwd('leptocephalus')
            | kwd('immatures') | kwd('immature')
            | kwd('imms') | kwd('imm')
            | kwd('young adult') | kwd('young')
            | kwd('ygs') | kwd('yg')
            | kwd('fleglings') | kwd('flegling')
            | kwd('fledgelings') | kwd('fledgeling')
            | kwd('chicks') | kwd('chick')
            | kwd('nestlings') | kwd('nestling')
            | kwd('juveniles') | kwd('juvenile')
            | kwd('juvéniles') | kwd('juvénile')
            | kwd('juvs') | kwd('juv')
            | kwd('jeunes') | kwd('jeune')
            | kwd('subadults') | kwd('subadult')
            | kwd('subadultes') | kwd('subadulte')
            | kwd('subads') | kwd('subad')
            | kwd('sub-adults') | kwd('sub-adult')
            | kwd('adults') | kwd('adult') | kwd('adulte')
            | kwd('ads') | kwd('ad')
            | kwd('yearlings') | kwd('yearling')
            | kwd('matures') | kwd('mature')
            | kwd('yolk sac') | kwd('yolksac')
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
