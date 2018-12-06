"""Parse the notations."""

from lib.parsers.base_parser import BaseParser
from lib.lexers.testes_state_lexer import LexerTestesState


class ParserTestesState(BaseParser):
    """Shared parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexerTestesState)

    def get_rules(self):
        """Return the parser rules."""
        return {
            'label not testes': self.value_in_1_and_2,
            'label scrotal': self.value_in_1,

            'label testes': 'record',
            'label abbrev': 'record',

            'record state_abbrev': self.value_in_1,
            'record not testes': self.value_in_1_and_2,
            'record descended': self.value_in_1,
            'record not descended': self.value_in_1_and_2,
            'record abdominal': self.value_in_1,
            'record abdominal not descended': self.value_in_1_thru_3,
            'record fully descended': self.value_in_1_and_2,
            'record partially descended': self.value_in_1_and_2,
            'record not fully descended': self.value_in_1_thru_3,
            'record scrotal': self.value_in_1,
            'record not scrotal': self.value_in_1_and_2,
            'record other_words': self.value_in_1_and_2,
            'record size': self.value_in_1,
            'record size not descended': self.value_in_1_thru_3,

            'testes descended': self.value_in_1,
            'testes abdominal': self.value_in_1,
            'testes scrotal': self.value_in_1,
            'testes abdominal not descended': self.value_in_1_thru_3,
            'testes not descended': self.value_in_1_and_2,
            'testes not fully descended': self.value_in_1_thru_3,
            'testes not scrotal': self.value_in_1_and_2,
            'testes other_words': self.value_in_1,
            'testes size not descended': self.value_in_1_thru_3,
            'testes state_abbrev': self.value_in_1,

            'abbrev descended': self.value_in_1,
            'abbrev abdominal': self.value_in_1,
            'abbrev scrotal': self.value_in_1,
            'abbrev abdominal not descended': self.value_in_1_thru_3,
            'abbrev not descended': self.value_in_1,
            'abbrev not fully descended': self.value_in_1_thru_3,
            'abbrev not scrotal': self.value_in_1_and_2,
            'abbrev other_words': self.value_in_1,
            'abbrev size not descended': self.value_in_1_thru_3,

            'not testes': self.value_in_0_and_1,
            'not scrotal': self.value_in_0_and_1,
            'not gonads': self.value_in_0_and_1}

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
