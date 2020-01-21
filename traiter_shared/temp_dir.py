"""Functions for dealing with temporary directories."""

import os
import sys
from contextlib import contextmanager
from tempfile import mkdtemp
from shutil import rmtree


def exists(temp_dir):
    """Make sure the temporary directory exits."""
    if temp_dir and not os.path.exists(temp_dir):
        sys.exit('The temporary directory must exist.')


def update(args, temp_dir):
    """Update the arguments and environment."""
    args.temp_dir = str(temp_dir)
    os.environ['SQLITE_TMPDIR'] = args.temp_dir


@contextmanager
def create(prefix, where=None, keep=False):
    """Handle creation and deletion of temporary directory."""
    temp_dir = mkdtemp(prefix=prefix, dir=where)
    try:
        yield temp_dir
    finally:
        if not keep or not where:
            rmtree(temp_dir)
