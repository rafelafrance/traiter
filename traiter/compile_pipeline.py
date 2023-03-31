#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib import pipeline

from traiter.pylib import log


def main():
    log.started()

    args = parse_args()

    pipeline.build(args.model_dir)

    log.finished()


def parse_args() -> argparse.Namespace:
    description = """Convert pattern objects into entity ruler patterns."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--model-dir",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Save the model to this directory.""",
    )

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
