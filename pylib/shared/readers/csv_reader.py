"""Read data from a CSV file."""

import pandas as pd
from .. import util
from .. import db


def read(args):
    """Read data from a CSV file."""
    print(args)

    reader = pd.read_csv(
        args.input_file, chunksize=util.BATCH_SIZE, na_filter=False, dtype=str)

    for i, df in enumerate(reader, 1):
        args.column = df.columns if args.all_columns else args.column

        df.loc[:, args.column].to_sql(
            'raw', db.connect(), if_exists='replace', index=False)
