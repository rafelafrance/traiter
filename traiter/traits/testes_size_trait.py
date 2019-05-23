"""Parse testes size notations."""

from operator import itemgetter
from stacked_regex.token import Token
from traiter.parse import Parse
from traiter.traits.base_trait import BaseTrait, ordinal
import traiter.shared_tokens as tkn


class TestesSizeTrait(BaseTrait):
    """Parser logic."""

    side_pairs = {'left': 'right', 'right': 'left', '1': '2', '2': '1'}

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)
        self._build_token_rules()
        self._build_product_rules()

        self.compile_regex()

    def _build_token_rules(self):
        self.shared_token(tkn.uuid)

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

        self.kwd('testes', r' testes |  testis | testicles? | test ')

        # Note: abbrev differs from the one in the testes_state_trait
        self.kwd('abbrev', r' tes | ts | tnd | td | tns | ta ')
        self.lit('char_key', r' \b t (?! [a-z] )')
        self.kwd('state', r"""
            scrotum | scrotal | scrot | nscr | scr | ns | sc
            | (?: not | non | no | semi | sub | un | partially | part
                    | fully | (:? in )? complete (?: ly)? )?
                (?: des?c?end (?: ed)? | desc? )
            | abdominal | abdomin | abdom | abd
            | visible | enlarged | small
            | gonads?
            | cryptorchism | cryptorchid | monorchism | monorchid | inguinal
            """)

        self.side = r' (?P<side> left | right | [lr] ) '
        self.kwd('lr', self.side)

        self.lr_delim = r' [/(\[] \s* (?P<side> [lr] ) \s* [)\]] '
        self.lit('lr_delim', self.lr_delim)

        self.shared_token(tkn.cross)
        self.lit('and', r' and | & ')
        self.lit('word', r' [a-z]+ ')
        self.lit('sep', r' [;] | $ ')

    def _build_product_rules(self):
        self.product(self.double, r"""
            label (?: testes | abbrev | char_key )
                (?P<first> (?: lr | lr_delim ) cross )
                (?P<second> (?: lr | lr_delim ) cross )?
            | label
                (?P<first> (?: lr | lr_delim ) cross )
                (?P<second> (?: lr | lr_delim ) cross )?
            | (?: testes | abbrev | char_key )
                (?P<first> (?: lr | lr_delim ) cross )
                (?P<second> (?: lr | lr_delim ) cross )?
            """)

        self.product(self.convert, r"""
            label (?: testes | abbrev | char_key ) cross
            | label (?: lr | lr_delim ) (?: testes | abbrev | char_key ) cross
            | label cross
            | label (?: testes | abbrev | state | word | sep | char_key){0,3}
                (?: testes | abbrev | state | char_key ) cross
            | (?: key_with_units | ambiguous ) cross
            | (?: key_with_units | ambiguous )
                (?: testes | abbrev | state | word | sep | char_key ){0,3}
                (?: testes | abbrev | state | char_key ) cross
            | testes (?: abbrev | state | word | sep | char_key ){0,3}
                (?: abbrev | state | char_key ) cross
            | testes (?: abbrev | state | word | char_key ) cross
            | (?: testes | state | abbrev ) cross
            | (?P<ambiguous_char> char_key ) cross
            """)

        # These are used to get compounds traits from a single parse
        self.double_side = self.compile(
            name='double_sided',
            regexp=f' (?P<double_side> {self.side} | {self.lr_delim} ) ')
        self.double_cross = self.compile(
            name='double_crossed',
            regexp=f' (?P<double_cross> {tkn.cross[1]} ) ')

        self.compile_regex()

    def double(self, token):
        """Convert a single token into multiple (two) traits."""
        if not token.groups.get('second'):
            return self.convert(token)

        # Regex second match groups will overwrite the first match groups
        trait2 = Parse(start=token.start, end=token.end)
        trait2.cross_value(token)
        trait2.is_value_in_token('side', token)

        # We need to re-extract the first match groups
        trait1 = Parse(start=token.start, end=token.end)

        groups = self.double_cross.find_matches(token.groups['first'])
        token1 = Token(groups=groups)
        trait1.cross_value(token1)

        groups = self.double_side.find_matches(token.groups['first'])
        token1 = Token(groups=groups)
        trait1.is_value_in_token('side', token1)

        return [trait1, trait2]

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        if token.groups.get('ambiguous_char') \
                and not token.groups.get('value2'):
            return None
        trait = Parse(start=token.start, end=token.end)
        trait.cross_value(token)
        trait.is_flag_in_token('ambiguous_char', token, rename='ambiguous_key')
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_value_in_token('dimension', token)
        trait.is_value_in_token('side', token)
        return trait

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

    @staticmethod
    def csv_formatter(trait, row, parses):
        """Format the trait for CSV output."""
        if not parses:
            return
        records = _build_records(parses)
        records = _merge_records(records)
        _format_records(records, row)


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


def _merge_flags(prev, curr):
    """If one of the flags is unambiguous then they all are."""
    prev['ambiguous_key'] |= curr['ambiguous_key']
    prev['units_inferred'] |= curr['units_inferred']


def _format_records(records, row):
    for i, rec in enumerate(records, 1):
        key = f'testes_{i}01:{ordinal(i)}_testes_side'
        row[key] = rec['side']
        key = f'testes_{i}20:{ordinal(i)}_testes_length'
        row[key] = rec['length'] if rec['length'] > 0 else ''
        key = f'testes_{i}21:{ordinal(i)} testes width'
        row[key] = rec['width'] if rec['width'] > 0 else ''
        if rec['ambiguous_key']:
            key = f'testes_{i}30:{ordinal(i)}_testes_ambiguous_key'
            row[key] = rec['ambiguous_key']
        if rec['units_inferred']:
            key = f'testes_{i}31:{ordinal(i)}_testes_units_inferred'
            row[key] = rec['units_inferred']
