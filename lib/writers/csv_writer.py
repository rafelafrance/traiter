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

        for trait, data in parsed_record.items():
            TRAITS[trait](row, data)

        self.rows.append(row)

    def end(self):
        """End the report."""
        dfm = pd.DataFrame(self.rows)
        dfm.to_csv(self.args.outfile, index=False)


def vocab_columns(row, data):
    """Output the trait into CSV columns."""
    for i, parse in enumerate(data, 1):
        row[f'sex_{i}'] = parse['value']
        flags = []
        for flag, value in parse['flags'].items():
            if value is True:
                flags.append(flag)
            else:
                flags.append(f'{flag}={value}')
        row[f'sex_{i}_flags'] = ', '.join(flags) if flags else ''


TRAITS = {
    'sex': vocab_columns,
    # 'life_stage': life_stage.to_csv,
    # 'total_length': total_length.to_csv,
    # 'tail_length': tail_length.to_csv,
    # 'hind_foot_length': hind_foot_length.to_csv,
    # 'ear_length': ear_length.to_csv,
    # 'body_mass': body_mass.to_csv,
    # 'testes_size': testes_size.to_csv,
    # 'testes_state': testes_state.to_csv,
}
