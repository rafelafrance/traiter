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
            column = f'{trait}_flag'
            row[column] = data['flags'].get('break', '')
            for i, parse in enumerate(data['parsed'], 1):
                for part in ('value', 'units', 'field', 'start', 'end'):
                    column = f'{trait}_{i}_{part}'
                    row[column] = parse[part]
                for flag, value in parse['flags'].items():
                    column = f'{trait}_{i}_{flag}'
                    row[column] = value

        self.rows.append(row)

    def end(self):
        """End the report."""
        pd.DataFrame(self.rows).to_csv(self.args.outfile, index=False)
