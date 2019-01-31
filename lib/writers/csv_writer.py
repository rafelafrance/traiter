"""Write the traiter output to a CSV file."""

import pandas as pd
from lib.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.index = 0
        self.rows = []
        self.columns = args.extra_field
        self.columns += args.search_field
        self.columns += sorted({f for fds in args.as_is.values() for f in fds})

    def start(self):
        """Start the report."""
        self.rows = []

    def record(self, raw_record, parsed_record):
        """Output a row to the file."""
        self.index += 1
        if self.args.log_every and self.index % self.args.log_every == 0:
            print(self.index)

        row = {c: raw_record.get(c, '') for c in self.columns}

        for trait, parses in parsed_record.items():
            TRAITS.get(trait, normal_trait)(trait, row, parses)

        self.rows.append(row)

    def end(self):
        """End the report."""
        dfm = pd.DataFrame(self.rows)
        dfm.to_csv(self.args.outfile, index=False)


def normal_trait(trait, row, parses):
    """Output the controlled vocabulary or numeric trait into CSV columns."""
    for i, parse in enumerate(parses, 1):
        if parse.get('value'):
            row[f'{trait}_{i}'] = parse['value']
        flags = []
        if parse.get('units') is not None:
            flags.append(f'original_units={parse["units"]}')
        for flag, value in parse['flags'].items():
            if value is True:
                flags.append(flag)
            else:
                flags.append(f'{flag}={value}')
        row[f'{trait}_{i}_notes'] = ', '.join(flags) if flags else ''


def testes_size(trait, row, parses):
    """Testes size requires special formatting for CSV output."""
    left, right = 0, 0
    for parse in parses:
        if parse.get('side') in ['right', '2']:
            side = 'right/2'
            right += 1
            count = right
        else:
            side = 'left/1'
            left += 1
            count = left

        name = f'{trait}_{side}_{count}'
        if parse.get('value'):
            row[name] = parse['value']

        flags = []
        if parse.get('units') is not None:
            flags.append(f'original_units={parse["units"]}')
        for flag, value in parse['flags'].items():
            if value is True:
                flags.append(flag)
            else:
                flags.append(f'{flag}={value}')

        row[f'{name}_notes'] = ', '.join(flags) if flags else ''


TRAITS = {
    'testes_size': testes_size,
}
