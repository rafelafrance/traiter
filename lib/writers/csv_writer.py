"""Write the traiter output to a CSV file."""

import csv
import json
from lib.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.writer = None
        self.columns = args.extra_field
        self.columns += ['results']
        self.columns += args.search_field
        self.columns += sorted({f for fds in args.as_is.values() for f in fds})

    def start(self):
        """Start the report."""
        self.writer = csv.DictWriter(self.outfile, self.columns)
        self.writer.writeheader()

    def record(self, row, results):
        """Output a row to the file."""
        row = {c: row.get(c, '') for c in self.columns}
        row['results'] = json.dumps(results)
        self.writer.writerow(row)

    def end(self):
        """End the report."""
        self.outfile.close()
