"""Read data from a CSV file."""

import pandas as pd


def read(args):
    """Read data from a CSV file."""
    print(args)

    columns = args.extra_field + args.search_field

    chunk = 1_000_000
    reader = pd.read_csv(
        args.input_file, chunksize=chunk, na_filter=False, dtype=str)

    for i, df in enumerate(reader, 1):
        df = df.drop(columns=[c for c in df.columns if c not in columns])
        print(df.head())
        print(df.shape)
