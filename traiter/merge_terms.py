#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

import pandas as pd


def main():
    args = parse_args()

    csvs = [
        pd.read_csv(f)
        for f in sorted(args.term_dir.glob("*.csv"))
        if f.stem not in args.exclude
    ]

    merged = pd.concat(csvs)
    merged = merged.sort_values(["label", "pattern"])
    merged.to_csv(args.merged_csv, index=False)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""Merge all terms into a single CSV file."""),
    )

    arg_parser.add_argument(
        "--term-dir",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Directory containing the term CSV files.""",
    )

    arg_parser.add_argument(
        "--merged-csv",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Output the merged data to this CSV file.""",
    )

    arg_parser.add_argument(
        "--exclude",
        metavar="STEM",
        action="append",
        help="""Exclude CSV files with these stems. Repeat for more than one file.""",
    )

    args = arg_parser.parse_args()

    args.exclude = args.exclude if args.exclude else []

    return args


if __name__ == "__main__":
    main()
