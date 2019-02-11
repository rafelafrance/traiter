"""Parse testes size notations."""

from operator import itemgetter
from lib.trait import Trait
from lib.traits.base_trait import BaseTrait, ordinal
import lib.shared_tokens as tkn


class TestesSizeTrait(BaseTrait):
    """Parser logic."""

    side_pairs = {'left': 'right', 'right': 'left', '1': '2', '2': '1'}

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        # Build the tokens
        self.kwd('label', r' reproductive .? (?: data | state | condition ) ')

        self.kwd('key_with_units', r"""
            (?P<ambiguous_key> gonad ) \s* (?P<dimension> length | width ) \s*
                in \s* (?P<units> millimeters | mm )
            """)

        self.kwd('ambiguous', r"""
            (?P<ambiguous_key> gonad ) \s* (?P<dimension> length | width )
                \s* (?: (?P<side> [12] ) |  )
            | (?P<side> left | right ) \s* (?P<ambiguous_key> gonad )
                \s* (?P<dimension> length | width )
            | (?P<ambiguous_key> gonad ) \s* (?P<dimension> length | width )
            """)

        self.kwd('testes', r' testes |  testis | testicles | test ')
        self.kwd('abbrev', r' tes | ts ')
        self.lit('char_key', r' \b t (?! [a-z] )')
        self.kwd('scrotal', r' scrotum | scrotal | scrot | nscr ')
        self.kwd('lr', r' (?P<side> left | right | l | r ) ')
        self.lit('lr_delim', r' [/(\[] \s* (?P<side> l | r ) \s* [)\]] ')
        self.shared_token(tkn.cross)
        self.lit('and', r' and | & ')
        self.lit('word', r' [a-z]+ ')
        self.lit('sep', r' [;,] | $ ')

        # Build rules for parsing the trait
        self.product(self.convert, r"""
            label (?: testes | abbrev | char_key ) cross
            | label (?: testes | abbrev | char_key ) (?: lr | lr_delim ) cross
            | (?: testes | abbrev | char_key ) (?: lr | lr_delim ) cross
            | label cross
            | label testes cross
            | label (?: testes | abbrev | scrotal | word | sep | char_key){1,3}
                (?: testes | abbrev | scrotal | char_key ) cross
            | (?: key_with_units | ambiguous ) cross
            | (?: key_with_units | ambiguous )
                (?: testes | abbrev | scrotal | word | sep | char_key ){1,3}
                (?: testes | abbrev | scrotal | char_key ) cross
            | testes (?: abbrev | scrotal | word | sep | char_key ){1,3}
                (?: abbrev | scrotal | char_key ) cross
            | testes (?: abbrev | scrotal | word | char_key ) cross
            | (?: testes | scrotal | abbrev ) cross
            | (?P<ambiguous_char> char_key ) cross
            """)

        self.finish_init()

    def convert(self, token):  # pylint: disable=no-self-use
        """Convert parsed token into a trait product."""
        if token.groups.get('ambiguous_char') \
                and not token.groups.get('value2'):
            return None
        trait = Trait(start=token.start, end=token.end)
        trait.cross_value(token)
        trait.is_flag_in_token('ambiguous_char', token, rename='ambiguous_key')
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_value_in_token('dimension', token)
        trait.is_value_in_token('side', token)
        return trait

    @staticmethod
    def csv_formater(trait, row, parses):
        """Format the trait for CSV output."""
        if not parses:
            return
        records = _build_records(parses)
        records = _merge_records(records)
        _format_records(records, row)

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'female':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'female'"
        return True

    @staticmethod
    def adjust_record(data, trait):
        """Adjust the trait based on other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return
        for parse in data[trait]:
            parse.ambiguous_key = False


def _merge_flags(prev, curr):
    prev['ambiguous_key'] |= curr['ambiguous_key']
    prev['units_inferred'] |= curr['units_inferred']


def _build_records(parses):
    records = []
    for parse in parses:
        if isinstance(parse.value, list):
            length, width = parse.value
            if width > length:
                length, width = width, length
        elif parse.dimension == 'width':
            length, width = -1, parse.value
        else:
            length, width = parse.value, -1
        records.append({'side': parse.side,
                        'length': length,
                        'width': width,
                        'ambiguous_key': parse.ambiguous_key,
                        'units_inferred': parse.units_inferred})
    return sorted(records, key=itemgetter('side', 'length', 'width'))


def _merge_records(records):
    merged = [records[0]]
    for curr in records:
        prev = merged[-1]
        if prev['side'] == curr['side']:
            if prev['length'] == curr['length'] \
                    and prev['width'] == curr['width']:
                _merge_flags(prev, curr)
                continue
            elif prev['length'] == -1 and curr['length'] != -1:
                prev['length'] = curr['length']
                _merge_flags(prev, curr)
                continue
            elif prev['width'] == -1 and curr['width'] != -1:
                _merge_flags(prev, curr)
                prev['width'] = curr['width']
                continue
        merged.append(curr)
    return merged


def _format_records(records, row):
    for i, rec in enumerate(records, 1):
        key = f'testes_{i}01:{ordinal(i)} testes side'
        row[key] = rec['side']
        key = f'testes_{i}20:{ordinal(i)} testes length'
        row[key] = rec['length'] if rec['length'] > 0 else ''
        key = f'testes_{i}21:{ordinal(i)} testes width'
        row[key] = rec['width'] if rec['width'] > 0 else ''
        if rec['ambiguous_key']:
            key = f'testes_{i}30:{ordinal(i)} testes ambiguous key'
            row[key] = rec['ambiguous_key']
        if rec['units_inferred']:
            key = f'testes_{i}31:{ordinal(i)} testes units inferred'
            row[key] = rec['units_inferred']
