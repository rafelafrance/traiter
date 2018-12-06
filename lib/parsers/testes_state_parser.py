"""Parse the notations."""

from lib.parsers.base_parser import BaseParser
from lib.lexers.testes_state_lexer import LexerTestesState


class ParserTestesState(BaseParser):
    """Shared parser logic."""

    def __init__(self):
        super().__init__(LexerTestesState)

    def get_rules(self):
        return {
            'label testes state': self.value_in_2,
            'label testes state_abbrev': self.value_in_2,
            'label testes not testes': self.value_in_2_and_3,
            'label testes descended': self.value_in_2,
            'label testes not descended': self.value_in_2_and_3,
            'label testes abdominal': self.value_in_2,
            'label testes abdominal not descended': self.value_in_2_thru_4,
            'label testes fully descended': self.value_in_2_and_3,
            'label testes partially descended': self.value_in_2_and_3,
            'label testes not fully descended': self.value_in_2_thru_4,
            'label testes scrotal': self.value_in_2,
            'label testes not scrotal': self.value_in_2_and_3,
            'label testes other_words': self.value_in_2_and_3,
            'label testes size': self.value_in_2,
            'label testes size not descended': self.value_in_2_thru_4,

            'label abbrev state': self.value_in_2,
            'label abbrev state_abbrev': self.value_in_2,
            'label abbrev not testes': self.value_in_2_and_3,
            'label abbrev descended': self.value_in_2,
            'label abbrev not descended': self.value_in_2_and_3,
            'label abbrev abdominal': self.value_in_2,
            'label abbrev abdominal not descended': self.value_in_2_thru_4,
            'label abbrev fully descended': self.value_in_2_and_3,
            'label abbrev partially descended': self.value_in_2_and_3,
            'label abbrev not fully descended': self.value_in_2_thru_4,
            'label abbrev scrotal': self.value_in_2,
            'label abbrev not scrotal': self.value_in_2_and_3,
            'label abbrev other_words': self.value_in_2_and_3,
            'label abbrev size': self.value_in_2,
            'label abbrev size not descended': self.value_in_2_thru_4,

            'testes descended': self.value_in_1,
            'testes abdominal': self.value_in_1,
            'testes scrotal': self.value_in_1,
            'testes abdominal not descended': self.value_in_1_thru_3,
            'testes not descended': self.value_in_1_and_2,
            'testes not scrotal': self.value_in_1_and_2,
            'testes other_words': self.value_in_1,
            'testes size not descended': self.value_in_1_thru_3,

            'abbrev descended': self.value_in_1,
            'abbrev abdominal': self.value_in_1,
            'abbrev scrotal': self.value_in_1,
            'abbrev abdominal not descended': self.value_in_1_thru_3,
            'abbrev not descended': self.value_in_1,
            'abbrev not scrotal': self.value_in_1_and_2,
            'abbrev other_words': self.value_in_1,
            'abbrev size not descended': self.value_in_1_thru_3,

            'not testes': self.value_in_0_and_1,
            'not scrotal': self.value_in_0_and_1,
            'not gonads': self.value_in_0_and_1,
        }

    def value_in_1(self, stack, input):
        result = {'value': stack[1]['value'],
                  'start': stack[0]['start'],
                  'end': stack[1]['end']}
        return result

    def value_in_0_and_1(self, stack, input):
        result = {'value': input[stack[0]['start']:stack[1]['end']],
                  'start': stack[0]['start'],
                  'end': stack[1]['end']}
        return result

    def value_in_1_and_2(self, stack, input):
        result = {'value': input[stack[1]['start']:stack[2]['end']],
                  'start': stack[0]['start'],
                  'end': stack[2]['end']}
        return result

    def value_in_1_thru_3(self, stack, input):
        result = {'value': input[stack[1]['start']:stack[3]['end']],
                  'start': stack[0]['start'],
                  'end': stack[3]['end']}
        return result

    def value_in_1_thru_4(self, stack, input):
        result = {'value': input[stack[1]['start']:stack[4]['end']],
                  'start': stack[0]['start'],
                  'end': stack[4]['end']}
        return result

    def value_in_2(self, stack, input):
        result = {'value': stack[2]['value'],
                  'start': stack[0]['start'],
                  'end': stack[2]['end']}
        return result

    def value_in_2_and_3(self, stack, input):
        result = {'value': input[stack[2]['start']:stack[3]['end']],
                  'start': stack[0]['start'],
                  'end': stack[3]['end']}
        return result

    def value_in_2_thru_4(self, stack, input):
        result = {'value': input[stack[2]['start']:stack[4]['end']],
                  'start': stack[0]['start'],
                  'end': stack[4]['end']}
        return result
