"""Read data from a CSV file."""

import pandas as pd
from pylib.shared import util
from pylib.shared import db


def read(args):
    """Read data from a CSV file."""
    reader = pd.read_csv(
        args.input_file, chunksize=util.BATCH_SIZE, na_filter=False, dtype=str)

    for i, df in enumerate(reader, 1):
        print(f'Importing chunk {i}')
        args.column = df.columns if args.all_columns else args.column

        with db.connect(args.db) as cxn:
            df.loc[:, args.column].to_sql(
                db.RAW_TABLE,
                cxn,
                if_exists='replace',
                index_label=db.RAW_ID)
