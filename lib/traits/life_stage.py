"""Parse life stage notations."""

from pyparsing import Regex, Word, Group
from lib.base import Base
from lib.result import Result
import lib.regexp as rx


class LifeStage(Base):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = (
            Group(rx.kwd('life') + rx.kwd('stage') + rx.kwd('remarks'))
            | Group(rx.kwd('lifestage') + rx.kwd('remarks'))
            | rx.kwd('lifestageremarks')
            | Group(rx.kwd('life') + rx.kwd('stage'))
            | rx.kwd('lifestage')
            | Group(rx.kwd('age') + rx.kwd('class'))
            | rx.kwd('ageclass')
            | Group(rx.kwd('age') + rx.kwd('in') + rx.kwd('hours'))
            | rx.kwd('ageinhours')
            | Group(rx.kwd('age') + rx.kwd('in') + rx.kwd('days'))
            | rx.kwd('ageindays')
            | rx.kwd('age')
        )

        years = (
            rx.kwd('first') | rx.kwd('second')
            | rx.kwd('third') | rx.kwd('fourth')
            | rx.kwd('1st') | rx.kwd('2nd') | rx.kwd('3rd') | rx.kwd('4th')
            | rx.kwd('hatching')
         )

        keyless = (
            Group(rx.kwd('after') + years + rx.kwd('year'))
            | Group(years + rx.kwd('year'))
            | rx.kwd('larves') | rx.kwd('larvae') | rx.kwd('larva')
            | rx.kwd('larvals') | rx.kwd('larval')
            | rx.kwd('imagos') | rx.kwd('imago')
            | rx.kwd('neonates') | rx.kwd('neonates')
            | rx.kwd('hatchlings') | rx.kwd('hatchling') | rx.kwd('hatched')
            | rx.kwd('fry')
            | rx.kwd('metamorphs') | rx.kwd('metamorph')
            | rx.kwd('premetamorphs') | rx.kwd('premetamorph')
            | rx.kwd('tadpoles') | rx.kwd('tadpole')
            | rx.kwd('têtard')
            | rx.kwd('young-of-the-year')
            | rx.kwd('leptocephales') | rx.kwd('leptocephale')
            | rx.kwd('leptocephalus')
            | rx.kwd('immatures') | rx.kwd('immature')
            | rx.kwd('imms') | rx.kwd('imm')
            | rx.kwd('young adult') | rx.kwd('young')
            | rx.kwd('ygs') | rx.kwd('yg')
            | rx.kwd('fleglings') | rx.kwd('flegling')
            | rx.kwd('fledgelings') | rx.kwd('fledgeling')
            | rx.kwd('chicks') | rx.kwd('chick')
            | rx.kwd('nestlings') | rx.kwd('nestling')
            | rx.kwd('juveniles') | rx.kwd('juvenile')
            | rx.kwd('juvéniles') | rx.kwd('juvénile')
            | rx.kwd('juvs') | rx.kwd('juv')
            | rx.kwd('jeunes') | rx.kwd('jeune')
            | rx.kwd('subadults') | rx.kwd('subadult')
            | rx.kwd('subadultes') | rx.kwd('subadulte')
            | rx.kwd('subads') | rx.kwd('subad')
            | rx.kwd('sub-adults') | rx.kwd('sub-adult')
            | rx.kwd('adults') | rx.kwd('adult') | rx.kwd('adulte')
            | rx.kwd('ads') | rx.kwd('ad')
            | rx.kwd('yearlings') | rx.kwd('yearling')
            | rx.kwd('matures') | rx.kwd('mature')
            | rx.kwd('yolk sac') | rx.kwd('yolksac')
        )

        word = Regex(r' \b (?! determin \w+ ) \w [\w?./-]* ', rx.flags)

        sep = Regex(r' [;,"?] | $ ', rx.flags)

        word_plus = keyless | word

        parser = (
            (keyword + (word_plus + Word('/-') + keyless)('value'))
            | (keyword + (word_plus*(1, 4))('value') + sep)
            | (keyword + (word_plus + keyless)('value'))
            | (keyword + keyless('value'))
            | keyless('value')
        )

        parser.ignore(Word(rx.punct, excludeChars='.,;"?/-'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        print(match)
        result = Result()
        result.vocabulary_value(match[0].value)
        result.ends(match[1], match[2])
        return result
