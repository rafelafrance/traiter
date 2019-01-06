"""Write the traiter output to a CSV file."""

import csv
# import json
# from dataclasses import asdict
from lib.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        super().__init__(args)
        self.columns = args.extra_field
        self.columns += [self.name(trait) for trait in args.trait]
        self.columns += args.search_field
        self.columns += sorted({f for fds in args.as_is.values() for f in fds})
        self.row = {}

    @staticmethod
    def name(trait):
        """Generate the CSV column name for the parsed trait."""
        return f'{trait}_results'

    def start(self):
        """Start the report."""
        self.writer = csv.DictWriter(self.outfile, self.columns)
        self.writer.writeheader()

    def start_row(self, row):
        """Start a report row."""
        self.row = {c: row.get(c, '') for c in self.columns}

    def cell(self, trait, results):
        """Build a report cell."""
        self.row[self.name(trait)] = results
        # if results:
        #     self.row[self.name(trait)] = json.dumps(
        #         [asdict(r) for r in results])

    def end_row(self):
        """End a report row."""
        print(self.row)
        print()
        # self.writer.writerow(self.row)

    def end(self):
        """End the report."""
        self.outfile.close()  # paranoia
