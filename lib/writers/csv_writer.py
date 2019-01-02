"""Write the traiter output to a CSV file."""

# import csv
# import json
from lib.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        self.args = args

    def start(self):
        """Start the report."""
        # writer = csv.DictWriter(args.outfile, fieldnames=all_columns)
        # writer.writeheader()
        # return writer

    def row(self):
        """Build a report row."""
        # writer.writerow(out_row)

    def cell(self):
        """Build a report cell."""
        # return json.dumps(parsed)

    def end(self):
        """End the report."""
        # Close output stream
