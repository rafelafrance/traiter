"""Write the traiter output to a CSV file."""

# import csv
# import json
from lib.writers.base_writer import BaseWriter


class CsvWriter(BaseWriter):
    """Write the traiter output to a file."""

    def start(self):
        """Start the report."""
        # self.reader = csv.DictReader(self.infile)
        # writer = csv.DictWriter(args.outfile, fieldnames=all_columns)
        # writer.writeheader()

    def cell(self, results):
        """Build a report cell."""
        print(results)
        # return json.dumps(parsed)

    def row(self):
        """Build a report row."""
        # writer.writerow(out_row)

    def end(self):
        """End the report."""
        self.outfile.close()  # paranoia
