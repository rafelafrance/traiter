"""Write the output to a CSV file."""


def csv_writer(args, families, df):  # pylint: disable=unused-argument
    """Output the data frame."""
    rows = [x.to_dict() for i, x in df.iterrows()]
    binomials = [r['taxon'] for r in rows if len(r['taxon'].split()) == 2]
    # print('sci_name')
    for binomial in sorted(binomials):
        print(f"'{binomial}',")
        # print(f"{binomial}")
        # print(f"or synonyms like '%{binomial}%'")

# import regex
# import pandas as pd
# # from pylib.all_traits import TRAITS
# from pylib.writers.base_writer import BaseWriter
#
#
# class CsvWriter(BaseWriter):
#     """Write the lib output to a file."""
#
#     def __init__(self, args):
#         """Build the writer."""
#         super().__init__(args)
#         self.limit = 4
#         self.columns = args.extra_field
#         self.columns += args.search_field
#       self.columns += sorted({f for fds in args.as_is.values() for f in fds})
#
#     def start(self):
#         """Start the report."""
#         self.rows = []
#
#     def record(self, raw_record, parsed_record):
#         """Output a row to the file."""
#         self.progress()
#
#         row = {c: raw_record.get(c, '') for c in self.columns}
#
#         # for trait, parses in parsed_record.items():
#         #     TRAITS[trait].csv_formatter(trait, row, parses[:self.limit])
#
#         self.rows.append(row)
#
#     def end(self):
#         """End the report."""
#         df = pd.DataFrame(self.rows)
#         df.rename(columns=lambda x: regex.sub(r'^.+?:\s*', '', x),
#               inplace=True)
#         df.to_csv(self.args.output_file, index=False)
